import threading
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.threads.resources import shapes, menu
from src.threads.frames import frame

class BackgroundFunction(threading.Thread):
  def __init__(self, function, args):
    self.done = False
    self.result = None

    self.function = function
    self.args = args
    threading.Thread.__init__(self)
    threading.Thread.start(self)

  def run(self):
    self.result = self.function(*self.args)
    self.done = True

class Loading(frame.Frame):
  def preGL(self):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity() 
    glViewport(0, 0, self.frameWidth, self.frameHeight)
    glOrtho(0, self.frameWidth, self.frameHeight, 0, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_DEPTH_BUFFER_BIT)

  def postGL(self):
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

  def animateDots(self):
    scale = 100
    self.animationCount %= scale

    self.dotState = [(0, 0, 0)] * (self.dots)
    for index in xrange(self.animationCount / (scale/(self.dots + 1))):
      if(index < self.dots):
        self.dotState[index] = (1, 1, 1)

  def drawDots(self):
    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    dy = self.dy

    radius = 5
    dx = 15
    width = dx * self.dots #+ 2 * radius
    offset = width / 2.0
    for circ in xrange(self.dots):
      shapes.Circle(cx + circ*dx - offset, cy + dy, radius,
                    [self.dotState[circ]]).draw()

  def drawSpinning(self):
    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    size = 50
    dy = self.dy

    color = (1, 1, 1)
    borderColor = (0, 0, 0)
    shapes.Rectangle(cx,cy-dy,size,size,color,self.spin,borderColor).draw()

  def draw(self):
    self.preGL()
    self.drawSpinning()
    self.drawDots()
    self.postGL()

  def timerFired(self, count):
    self.spin += 1
    self.animationCount += 1
    if(self.backgroundTask.done):
      self.dispRef.currentFrame = self.nextFrame

  def __init__(self, displayRef, frameSize, nextFrame, backgroundFunc,
                 args = []):
    super(Loading, self).__init__(displayRef, frameSize)
    self.nextFrame = nextFrame
    self.backgroundTask = BackgroundFunction(backgroundFunc, args)

    self.spin = 0
    self.dots = 5
    self.dotState = [(0, 0, 0)] * (self.dots)
    self.animationCount = 0
    self.dy = 40
