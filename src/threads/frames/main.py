from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time

from src.threads.frames import frame
from src.threads.resources import shapes, buttons, menu

class MainMenu(frame.Frame):
  clearColor = (.5, .5, .5, 1)
  defaultColor = (1.0, 1.0, 1.0)

  delay = (1.0/24.0)

  PLAY = 1
  DOWNLOAD = 2
  ABOUT = 3
  LOGO = 4

  def preGL(self):
    glDisable(GL_DEPTH_TEST)
    glClearColor(*MainMenu.clearColor)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(*MainMenu.defaultColor)
    glLoadIdentity()

  def draw(self):
    self.preGL()
    self.menu.draw()
    time.sleep(MainMenu.delay)

  def timerFired(self, value):
    pass

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)

  def keyboard(self, key, x, y):
    pass

  def specialKeys(self, key, x, y):
    pass

  def __init__(self, frameSize):
    super(MainMenu, self).__init__(frameSize)
    (cx, cy) = (self.width / 2.0, self.height / 2.0)
    dx = 110
    dy = 75
    objs  = [buttons.TexturedButton(cx - dx, cy + dy, MainMenu.PLAY,"play.png"),
             buttons.TexturedButton(cx,cy+dy,MainMenu.DOWNLOAD,"download.png"),
             buttons.TexturedButton(cx + dx,cy + dy,MainMenu.ABOUT,"about.png"),
             buttons.TexturedButton(cx, cy - dy, MainMenu.LOGO, "TM.png")]
    self.menu = menu.Menu(self.frameSize, objs)
