from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import time
import math

from src.threads.resources import buttons
from src.threads.frames import sim, menus

class Worker(object):
  frameName = "-= TerraMotus =-"
  width = 1080
  height = 720
  frameSize = (width, height)

  clearColor = (1, 1, 1, 1)

  # Milliseconds
  updateDelay = 42

  def preGL(self):
    glShadeModel(GL_FLAT)

  def postGL(self):
    glutSwapBuffers()
  
  def timerFired(self, value):
    self.currentFrame.timerFired(value)
    glutTimerFunc(Worker.updateDelay, self.timerFired, value)

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.currentFrame.mouse(mouseButton, buttonState, x, y)

  def keyboard(self, key, x, y):
    self.currentFrame.keyboard(key, x, y)

  def specialKeys(self, key, x, y):
    self.currentFrame.specialKeys(key, x, y)

  def draw(self):
    self.preGL()
    self.currentFrame.draw()
    self.postGL()

  def reshape(self, width, height):
    if(self.width != width or self.height != height):
      glutReshapeWindow(self.width, self.height)

  def close(self):
    freenect.sync_stop()

  def runGL(self):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(*Worker.frameSize)
    glutCreateWindow(Worker.frameName)
  
    glutDisplayFunc(self.draw)
    glutIdleFunc(self.draw)
    glutTimerFunc(Worker.updateDelay, self.timerFired, 0)
    glutMouseFunc(self.mouse)
    glutKeyboardFunc(self.keyboard)
    glutSpecialFunc(self.specialKeys)
    glutReshapeFunc(self.reshape)

    try:
      glutCloseFunc(self.close)
    except:
      glutWMCloseFunc(self.close)

    # Blocks
    glutMainLoop()
   
  def __init__(self, args):
    self.mapDir = "maps"
    self.imageDir = "images"
    self.resourceDir = "resources"
    self.sim = sim.Simulation(self, Worker.frameSize, self.mapDir)
    self.currentFrame = menus.MainMenu(self, Worker.frameSize)

    self.runGL()
