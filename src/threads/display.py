from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import math

class Worker(object):
  graphicsQueue = None

  def __init__(self, graphicsQueue, physicsThread):
    self.graphicsQueue = graphicsQueue
    glClearColor(*data.backgroundColor)
    glShadeModel(GL_FLAT)

  def keyPressed(self, key, x, y):
    pass

  def resizeRequest(self, width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.3333, 0.2, 200)
    glMatrixMode(GL_MODELVIEW)

  def prep(self):
    glClear(GL_COLOR_BUFFER_BIT)
    # White
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.3333, 0.2, 200)
    glMatrixMode(GL_MODELVIEW)

  def cleanUp(self):
    glutSwapBuffers()

  def drawTriMesh(self):
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

  def drawCar(self):
    pass
 
  def drawHUD(self):
    pass

  def drawAll(self):
    self.prep()
    #self.drawTriMesh()
    #self.drawCar()
    #self.drawHUD()
    self.cleanUp()

  def setCameraPos(x, y, z):
    pass

  def setCameraRot(roll, pitch, yaw):
    pass
    gluLookAt (25, 25, 5, 26, 26, 3, 0, 0, 1)
