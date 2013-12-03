from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Frame(object):
  clearColor = (0, 0, 0, 0)
  defaultColor = (1, 1, 1)

  def preGL(self):
    glClearColor(*self.clearColor)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(*self.defaultColor)
    glLoadIdentity()
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    glMatrixMode(GL_MODELVIEW)

  def draw(self):
    self.preGL()
 
  def timerFired(self, value): pass
  def mouse(self, mouseButton, buttonState, x, y): pass
  def keyboard(self, key, x, y): pass
  def specialKeys(self, key, x, y): pass

  def __init__(self, displayRef, frameSize):
    self.dispRef = displayRef
    (self.width, self.height) = self.frameSize = frameSize
