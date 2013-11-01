from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import time
import math

class Worker(object):
  frameName = "-= TerraMotus =-"
           # Width, Height
  frameSize = (640, 480)
  
  # World Properties
  # A nice light blue
  skyColor = (0.0, 178.0/255.0, 255.0/255.0, 255.0/255.0)

  # White with no opacity
  defaultColor = (1.0, 1.0, 1.0)

  def preGL(self):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(*Worker.defaultColor)
    glLoadIdentity()
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Degree of FOV, width / height ratio, min dist, max dist
    gluPerspective(45, 1.3333, 0.2, 200)
    glMatrixMode(GL_MODELVIEW)
  
  def postGL(self):
    glutSwapBuffers()
  
  def setCamera(self, x, y, z, roll, pitch, yaw):
    gluLookAt (30, 30, 30, 0, 0, 0, 0, 0, 1)
  
  def drawTriMesh(self, dataPlane):
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
  
  def drawFrame(self):
    self.preGL()
  
    if(not(self.dataThread.graphicsQueue.empty())):
      self.dataPlane = self.dataThread.graphicsQueue.get()
    
    glPushMatrix()
    glTranslatef(-self.dataPlane.width/2.0, -self.dataPlane.height/2.0, 0)
    
    self.drawTriMesh(self.dataPlane)

    glPopMatrix()
  
    time.sleep(1.0/30.0)
    self.postGL()
  
  def reshape(self, width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.3333, 0.2, 200)
    glMatrixMode(GL_MODELVIEW)
  
  def initGL(self):
    if(not(self.dataThread.graphicsQueue.empty())):
      self.dataPlane = self.dataThread.graphicsQueue.get()
    else:
      print "Error! Data should be here by now!"
      exit()
  
    glClearColor(*Worker.skyColor)
    glShadeModel(GL_FLAT)
  
  def runGL(self):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(*Worker.frameSize)
    glutCreateWindow(Worker.frameName)
  
    self.initGL()
  
    glutDisplayFunc(self.drawFrame)
    glutIdleFunc(self.drawFrame)
    glutReshapeFunc(self.reshape)
  
    # Blocks
    glutMainLoop()
  
  def __init__(self, dataThread, physicsThread):
    self.dataThread = dataThread
    self.physicsThread = physicsThread
    self.dataPlane = None

    self.eyeX     = 0
    self.eyeY     = 0
    self.eyeZ     = 0

    self.eyeRoll  = 0
    self.eyePitch = 0
    self.eyeYaw   = 0

    self.runGL()
