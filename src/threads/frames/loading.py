from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.threads.resources import shapes, menu

class Loading(menu.Menu):
  def animateDots(self):
    pass

  def drawDots(self):
    (cx, cy) = (self.width / 2.0, self.height / 2.0)
    dy = 25

    radius = 5
    dx = 15
    width = dx * self.dots #+ 2 * radius
    offset = width / 2.0
    for circ in xrange(self.dots):
      shapes.Circle(cx + circ*dx - offset, cy + dy, radius,
                    [self.dotState[circ]]).draw()

  def drawSpinning(self):
    (cx, cy) = (self.width / 2.0, self.height / 2.0)
    dy = 25

    color = (1, 1, 1)
    borderColor = (0, 0, 0)

    shapes.Rectangle(cx, cy - dy, 20, 20, color, self.spin, borderColor).draw()

  def draw(self):
    self.preGL()
    self.drawSpinning()
    self.drawDots()
    #self.spin += 1

  def timerFired(self, count):
    self.spin += 1

  def mouse(self, mouseButton, buttonState, x, y): pass

  def __init__(self, frameSize):
    super(Loading, self).__init__(frameSize, [])
    self.spin = 0
    self.dots = 5
    self.dotState = [(0, 0, 0)] * (self.dots)
