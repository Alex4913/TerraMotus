from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.threads.resources import shapes, menu
from src.threads.frames import frame

class Loading(frame.Frame):
  def animateDots(self):
    scale = 100
    self.animationCount %= scale

    self.dotState = [(0, 0, 0)] * (self.dots)
    for index in xrange(self.animationCount / (scale/(self.dots + 1))):
      if(index < self.dots):
        self.dotState[index] = (1, 1, 1)

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

  def timerFired(self, count):
    self.spin += 1
    self.animationCount += 1
    self.done = self.backgroundThread.ready

  def mouse(self, mouseButton, buttonState, x, y): pass

  def __init__(self, displayRef, frameSize):#, backgroundThread):
    super(Loading, self).__init__(displayRef, frameSize)
    self.spin = 0
    self.dots = 5
    self.dotState = [(0, 0, 0)] * (self.dots)

#    self.backgroundThread = backgroundThread
 #   self.backgroundThread.start()
