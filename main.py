#!/usr/bin/python
import sys
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
  while(instance.dataPlane is None):
    continue
  print "   -> Got it!"

  print " -> Starting engine..."
  instance.start()
  print "   -> Choo choo, mothafucka!"

  return instance

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
  gluLookAt (30, 30, 30, 0, 0, 0, 0, 0, 1)

def postGL():
  glutSwapBuffers()

def setCamera(x, y, z, roll, pitch, yaw):
  glRotate(-r, 1, 0, 0)
  glRotate(-p, 0, 1, 0)
  glRotate(-w, 0, 0, 1)
  glTranslatef(-x, -y, -z)

def drawTriMesh(dataPlane):
  verts = vbo.VBO(numpy.array(dataPlane.toVBO(), 'f'))

  colorRaw = [(1.0, 1.0, 1.0), (0, 0, 0)]*(len(dataPlane.toVBO())/2)

  color = vbo.VBO(numpy.array(colorRaw, 'f'))

  try:
    glEnableClientState(GL_COLOR_ARRAY)
    color.bind()
    try:
      glColorPointer(3, GL_FLOAT, 0, color)
    except: pass

    glEnableClientState(GL_VERTEX_ARRAY)
    verts.bind()
    try:
      glVertexPointer(3, GL_FLOAT, 0, verts)
      glDrawArrays(GL_TRIANGLES, 0, len(dataPlane.toVBO()))
    except Exception as e:
      print e
    finally:
      glDisableClientState(GL_COLOR_ARRAY)
      glDisableClientState(GL_VERTEX_ARRAY)
      verts.unbind()
      color.unbind()
  except Exception as e:
    print e

def drawFrame():
  preGL()

  glPushMatrix()
  if(not(data.dataThread.graphicsQueue.empty())):
    data.dataPlane = data.dataThread.graphicsQueue.get()
  glTranslatef(-data.dataPlane.width/2.0, -data.dataPlane.height/2.0, 0)
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
  gluLookAt (50, 50, 50, 0, 0, 0, 0, 0, 1)


def runGL(data):
  glutInit()
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
  glutInitWindowSize (640, 480)
  glutCreateWindow("-= TerraMotus =-")

  initGL(data)

  glutDisplayFunc(drawFrame)
  glutIdleFunc(drawFrame)
  glutReshapeFunc(reshape)

  glutMainLoop()


def init(args):
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

  dataThread = initCSVReader() if("--no-kinect" in args) else initKinect()
  physicsThread = initPhysics(dataThread.physicsQueue)

  return (dataThread, physicsThread)

def main():
  (dataThread, physicsThread) = init(sys.argv)

  global data
  class Empty(object): pass
  data = Empty()

  data.dataThread = dataThread
  data.physicsThread = physicsThread
  # Sky Blue
  data.backgroundColor = (0.0, 178.0/255.0, 255.0/255.0, 255.0/255.0)

  runGL(data)
  time.sleep(60)
  print "Exiting"
  for thread in (dataThread, physicsThread):
    thread.stop()

main()
