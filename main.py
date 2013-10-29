#!/usr/bin/python
import time

from src.threads import kinect, csvreader, engine
from src.tools import plane

###############################################################################
###                             Thread Init                                 ###
###############################################################################

def initCSVReader():
  print
  print "Emulating Kinect with CSVReader Thread"
  instance = csvreader.Worker()

  if(not(instance.fileExists)):
    print " -> No data in " + instance.fileName + "! Aborting."
    instance.stop()
    exit()

  print " -> Reading in CSV"
  instance.start()
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)
  print "   -> Got it!"
  return instance

def initKinect():
  print
  print "Starting Kinect Thread"

  instance = kinect.Worker()
  instance.start()

  print " -> Checking for Kinect-ivity..."
  startTime = time.time()
  while(not(instance.kinectDetected) and time.time() - startTime <= 5):
    time.sleep(0.100)

  if(not(instance.kinectDetected)):
    print "   -> Not Found! Using CSVReader instead"
    time.sleep(0.1)
    instance.stop()
    return initCSVReader()
  print "   -> Found!"

  print " -> Waiting for initial data..."
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)
  print "   -> Got it!"

  return instance

def initPhysics(physicsQueue):
  print
  print "Starting Physics Engine"

  instance = engine.Worker(physicsQueue)
  print " -> Checking for data..."
  while(not(instance.dataPlaneUpdated)):
    continue
  print "   -> Got it!"

  print " -> Starting engine..."
  instance.start()
  print "   -> Choo choo!"

  return instance

###############################################################################
###############################################################################

###############################################################################
###                                 GL Init                                 ###
###############################################################################

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import math

data = None

def initGL(data):
  if(not(data.dataThread.graphicsQueue.empty())):
    data.dataPlane = data.dataThread.graphicsQueue.get()
  else:
    assert(False)

  glClearColor(*data.backgroundColor)
  glShadeModel(GL_FLAT)

def preGL():
  glClear(GL_COLOR_BUFFER_BIT)
  # White
  glColor3f(1.0, 1.0, 1.0)
  glLoadIdentity()
  
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(45, 1.3333, 0.2, 200)
  glMatrixMode(GL_MODELVIEW)

def postGL():
  glutSwapBuffers()

def setCamera(x, y, z, roll, pitch, yaw):
  glRotate(-r, 1, 0, 0)
  glRotate(-p, 0, 1, 0)
  glRotate(-w, 0, 0, 1)
  glTranslatef(-x, -y, -z)

def drawTriMesh(dataPlane):
  shapes = vbo.VBO(numpy.array(dataPlane.toRawVertices(), 'f'))

  try:
    shapes.bind()
    try:
      glEnableClientState(GL_VERTEX_ARRAY)
      glVertexPointerf(shapes)
      glDrawArrays(GL_TRIANGLES, 0, len(dataPlane.toRawVertices()))
    finally:
      shapes.unbind()
      glDisableClientState(GL_VERTEX_ARRAY)
  except:
    print "Oh No!"

def drawFrame(data):
  preGL()

  glPushMatrix()
  glTranslatef(-data.dataPlane.height/2.0, -data.dataPlane.width/2.0, 0)
  drawTriMesh(data.dataPlane)
  glPopMatrix()

  time.sleep(1.0/30.0)
  postGL()

def reshape(width, height):
  glViewport(0, 0, width, height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(45, 1.3333, 0.2, 200)
  glMatrixMode(GL_MODELVIEW)
  gluLookAt (25, 25, 5, 26, 26, 3, 0, 0, 1)


def runGL(data):
  glutInit()
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
  glutInitWindowSize (640, 480)
  glutCreateWindow("-= TerraMotus =-")

  initGL(data)

  glutDisplayFunc(lambda func : drawFrame(data))
  glutIdleFunc(lambda func : drawFrame(data))
  glutReshapeFunc(lambda func : drawFrame(data))

  glutMainLoop()


def init():
  print
  print "          _____ "
  print "       .-'.  ':'-.       ______" 
  print "     .''::: .:    '.    /_  __/__ ___________ _"
  print "    /   :::::'      \    / / / -_) __/ __/ _ `/"
  print "   ;.    ':' `       ;  /_/__\\__/_/ /_/__\\_,_/"
  print "   |       '..       |    /  |/  /__  / /__ ______"
  print "   ; '      ::::.    ;   / /|_/ / _ \\/ __/ // (_-<"
  print "    \       '::::   /   /_/  /_/\\___/\\__/\\_,_/___/"
  print "     '.      :::  .'"
  print "       '-.___'_.-'"
  print

  dataThread = initKinect()
  physicsThread = initPhysics(dataThread.physicsQueue)

  return (dataThread, physicsThread)

def main():
  (dataThread, physicsThread) = init()

  global data
  class Empty(object): pass
  data = Empty()

  data.dataThread = dataThread
  data.physicsThread = physicsThread
  # Sky Blue
  data.backgroundColor = (0.0, 178.0/255.0, 255.0/255.0, 255.0/255.0)

  runGL(data)
  print "Exiting"
  for thread in (dataThread, physicsThread):
    thread.stop()

main()
