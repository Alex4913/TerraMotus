from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time

from src.threads.frames import frame
from src.threads.resources import shapes, buttons

class Menu(frame.Frame):
  def preGL(self):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity() 
    glViewport(0, 0, self.width, self.height)
    glOrtho(0, self.width, self.height, 0, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_DEPTH_BUFFER_BIT)
  
  def postGL(self):
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

  def draw(self):
    self.preGL()

    for obj in self.objects:
      obj.draw()

  def mouse(self, mouseButton, mouseState, x, y):
    pushed = []
    for obj in self.objects:
      if(isinstance(obj, buttons.Button)):
        if(obj.registerEvent(mouseButton, mouseState, x, y)):
          pushed += [obj]

    self.buttonEvents = pushed

  def __init__(self, dispRef, frameSize, objects = []):
    super(Menu, self).__init__(dispRef, frameSize)
    self.objects = objects
    self.buttonEvents = []
