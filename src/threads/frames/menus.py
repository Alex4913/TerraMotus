from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time
import os

from src.threads.frames import frame, loading
from src.threads.resources import shapes, buttons, menu, text
from src.threads import sources
from src.tools import client

class MainMenu(frame.Frame):
  delay = (1.0/24.0)

  PLAY = 1
  DOWNLOAD = 2
  ABOUT = 3
  LOGO = 4

  def draw(self):
    self.preGL()
    self.menu.draw()
    self.menu.postGL()
    time.sleep(MainMenu.delay)

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)

      if(MainMenu.PLAY in self.buttonsPressed):
        self.dispRef.currentFrame = ChooseInput(self.dispRef, self.frameSize)
      elif(MainMenu.DOWNLOAD in self.buttonsPressed):
        self.dispRef.currentFrame = DownloadCSV(self.dispRef, self.frameSize)
      elif(MainMenu.ABOUT in self.buttonsPressed):
        self.dispRef.currentFrame = AboutMenu(self.dispRef, self.frameSize)

  def __init__(self, dispRef, frameSize):
    super(MainMenu, self).__init__(dispRef, frameSize)
    self.clearColor = (.5, .5, .5, 1)
    self.defaultColor = (1.0, 1.0, 1.0)

    #if(not(client.Client(self.
    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    dx = 110
    dy = 75
    if(not(client.Client(self.dispRef.mapDir, self.dispRef.imageDir).ping())):
      dx = 65
      objs = [shapes.Texture(cx, cy, "background.png"),
             buttons.TexturedButton(cx - dx, cy + dy, MainMenu.PLAY,"play.png"),
             buttons.TexturedButton(cx + dx,cy + dy,MainMenu.ABOUT,"about.png"),
             buttons.TexturedButton(cx, cy - dy, MainMenu.LOGO, "logo.png")]
    else:
      objs = [shapes.Texture(cx, cy, "background.png"),
             buttons.TexturedButton(cx - dx, cy + dy, MainMenu.PLAY,"play.png"),
             buttons.TexturedButton(cx,cy+dy,MainMenu.DOWNLOAD,"download.png"),
             buttons.TexturedButton(cx + dx,cy + dy,MainMenu.ABOUT,"about.png"),
             buttons.TexturedButton(cx, cy - dy, MainMenu.LOGO, "logo.png")]
    self.menu = menu.Menu(self.dispRef, self.frameSize, objs)

class ChooseInput(frame.Frame):
  clearColor = (.5, .5, .5, 1)
  defaultColor = (1.0, 1.0, 1.0)

  delay = (1.0/24.0)

  KINECT = 1
  CSV = 2
  RESUME = 3
  HOME = 4

  def draw(self):
    self.preGL()
    self.menu.draw()
    self.menu.postGL()
    time.sleep(ChooseInput.delay)

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)
      
      if(ChooseInput.KINECT in self.buttonsPressed):
        func = self.dispRef.sim.setup 
        self.dispRef.currentFrame = loading.Loading(self.dispRef,
          self.frameSize, self.dispRef.sim, func, 
          [sources.KinectSource()])
      elif(ChooseInput.CSV in self.buttonsPressed):
        self.dispRef.currentFrame = ChooseCSV(self.dispRef, self.frameSize)
      elif(ChooseInput.RESUME in self.buttonsPressed):
        self.dispRef.sim.pause(False)
        self.dispRef.currentFrame = self.dispRef.sim
      elif(ChooseInput.HOME in self.buttonsPressed):
        self.dispRef.currentFrame = MainMenu(self.dispRef, self.frameSize)

  def __init__(self, dispRef, frameSize):
    super(ChooseInput, self).__init__(dispRef, frameSize)
    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    dx2 = 110
    dx3 = 210
    offset = 30

    objs = [shapes.Texture(cx, cy, "background.png")]
    if(not(sources.KinectSource().detect())):
      if(self.dispRef.sim.setuped):
       objs+=[buttons.TexturedButton(cx-dx2, cy, ChooseInput.CSV, "csv.png"),
              buttons.TexturedButton(cx+dx2,cy,ChooseInput.RESUME,"resume.png")]
      else:
       objs += [buttons.TexturedButton(cx,cy,ChooseInput.CSV,"csv.png")]
    else:
      if(self.dispRef.sim.setuped):
       objs+=[buttons.TexturedButton(cx-dx3,cy,ChooseInput.KINECT,"kinect.png"),
              buttons.TexturedButton(cx, cy, ChooseInput.CSV, "csv.png"),
              buttons.TexturedButton(cx+dx3,cy,ChooseInput.RESUME,"resume.png")]
      else:
       objs+=[buttons.TexturedButton(cx-dx2,cy,ChooseInput.KINECT,"kinect.png"),
              buttons.TexturedButton(cx + dx2, cy, ChooseInput.CSV, "csv.png")]
 

    objs += [buttons.TexturedButton(offset, self.frameHeight - offset,
                                      ChooseInput.HOME, "home.png")]
 
    self.menu = menu.Menu(self.dispRef, self.frameSize, objs)

class AboutMenu(frame.Frame):
  clearColor = (.5, .5, .5, 1)
  defaultColor = (1.0, 1.0, 1.0)

  delay = (1.0/24.0)

  HOME = 1

  def draw(self):
    self.preGL()

    self.menu.draw()
    self.menu.postGL()
    time.sleep(AboutMenu.delay)

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)
      if(AboutMenu.HOME in self.buttonsPressed):
        self.dispRef.currentFrame = MainMenu(self.dispRef, self.frameSize)

  def __init__(self, dispRef, frameSize):
    super(AboutMenu, self).__init__(dispRef, frameSize)
    offset = 30

    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    objs = [shapes.Texture(cx, cy, "background.png"),
            buttons.TexturedButton(offset, self.frameHeight - offset,
              AboutMenu.HOME, "home.png"),
            shapes.Texture(cx, cy, "info.png")]

    self.menu = menu.Menu(self.dispRef, self.frameSize, objs)

class ChooseCSV(frame.Frame):
  clearColor = (.5, .5, .5, 1)
  defaultColor = (1.0, 1.0, 1.0)

  delay = (1.0/24.0)

  HOME = 1
  UP = 2
  DOWN = 3

  def drawDynamic(self):
    self.genVisible()
    for item in self.visible:
      for component in item:
        component.draw()

  def genVisible(self):
    self.visible = []
    numCSVs = len(self.availableCSVs)
    limit = numCSVs if(self.shown >= numCSVs) else self.shown
    for item in xrange(limit):
      self.visible += [self.genEntry(item, limit)]

  def genEntry(self, num, limit):
    boxColor = (1, 1, 1)
    textColor = (0, 0, 0)
    borderColor = (0 ,0, 0)
    rHeight, rWidth = (50, 700)

    section = rHeight + 20
    tHeight = section * limit - section/2.0
    path = self.availableCSVs[(num + self.start) % len(self.availableCSVs)]
    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)

    return [buttons.RectangleButton(cx, cy + num*section - tHeight/2.0,
              rHeight,rWidth,(num + self.start) % len(self.availableCSVs),path),
            text.Text(GLUT_BITMAP_9_BY_15, path, textColor, cx, 
              cy +num*section-tHeight/2.0)]

  def draw(self):
    self.preGL()

    self.menu.draw()
    self.drawDynamic()
    self.menu.postGL()
    time.sleep(ChooseCSV.delay)

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)
      
      for item in self.visible:
        for component in item:  
          if(isinstance(component, buttons.Button)):
            if(component.registerEvent(mouseButton, buttonState, x, y)):
              func = self.dispRef.sim.setup 
              self.dispRef.currentFrame = loading.Loading(self.dispRef,
                self.frameSize, self.dispRef.sim, func, 
                [sources.CSVSource(component.text, self.dispRef.mapDir)])
 
      if(ChooseCSV.HOME in self.buttonsPressed):
        self.dispRef.currentFrame = MainMenu(self.dispRef, self.frameSize)
      elif(ChooseCSV.UP in self.buttonsPressed):
        self.start -= 1 if(self.start > 0) else 0
      elif(ChooseCSV.DOWN in self.buttonsPressed):
        self.start += 1 if(self.start+self.shown<len(self.availableCSVs)) else 0

  def __init__(self, dispRef, frameSize):
    super(ChooseCSV, self).__init__(dispRef, frameSize)
    offset = 30

    self.start = 0
    self.shown = 8
    self.visible = []
    self.availableCSVs = sorted(os.listdir(self.dispRef.mapDir))

    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    objs = [shapes.Texture(cx, cy, "background.png"),
            buttons.TexturedButton(offset, self.frameHeight - offset,
              ChooseCSV.HOME, "home.png")]

    if(len(self.availableCSVs) > self.shown):
      objs += [buttons.TriangleButton(self.frameWidth - 4*offset, cy + 4*offset,
                ((0, 50), (-25, 0), (25, 0)), ChooseCSV.DOWN,""),
               buttons.TriangleButton(self.frameWidth - 4*offset, cy - 5*offset,
              ((0, -50), (-25, 0), (25, 0)), ChooseCSV.UP,"")]

    self.menu = menu.Menu(self.dispRef, self.frameSize, objs)

class DownloadCSV(frame.Frame):
  clearColor = (.5, .5, .5, 1)
  defaultColor = (1.0, 1.0, 1.0)

  delay = (1.0/24.0)

  HOME = 1
  UP = 2
  DOWN = 3

  def drawDynamic(self):
    self.genVisible()
    for item in self.visible:
      for component in item:
        component.draw()

  def genVisible(self):
    self.visible = []
    numCSVs = len(self.availableCSVs)
    limit = numCSVs if(self.shown >= numCSVs) else self.shown
    for item in xrange(limit):
      self.visible += [self.genEntry(item, limit)]

  def genEntry(self, num, limit):
    boxColor = (1, 1, 1)
    textColor = (0, 0, 0)
    borderColor = (0 ,0, 0)
    rHeight, rWidth = (50, 700)

    section = rHeight + 20
    tHeight = section * limit - section/2.0
    path = self.availableCSVs[(num + self.start) % len(self.availableCSVs)]
    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)

    return [buttons.RectangleButton(cx, cy + num*section - tHeight/2.0,
              rHeight,rWidth,(num + self.start) % len(self.availableCSVs),path),
            text.Text(GLUT_BITMAP_9_BY_15, path, textColor, cx, 
              cy +num*section-tHeight/2.0)]

  def draw(self):
    self.preGL()

    self.menu.draw()
    self.drawDynamic()
    self.menu.postGL()
    time.sleep(DownloadCSV.delay)

  def getAndSetup(self, path):
    self.client.recv(path)
    self.dispRef.sim.setup(sources.CSVSource(path, 
                                             self.dispRef.mapDir))

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)
      
      for item in self.visible:
        for component in item:  
          if(isinstance(component, buttons.Button)):
            if(component.registerEvent(mouseButton, buttonState, x, y)):
              func = self.getAndSetup
              self.dispRef.currentFrame = loading.Loading(self.dispRef,
                self.frameSize, self.dispRef.sim, func, 
                [component.text])
 
      if(DownloadCSV.HOME in self.buttonsPressed):
        self.dispRef.currentFrame = MainMenu(self.dispRef, self.frameSize)
      elif(DownloadCSV.UP in self.buttonsPressed):
        self.start -= 1 if(self.start > 0) else 0
      elif(DownloadCSV.DOWN in self.buttonsPressed):
        self.start += 1 if(self.start+self.shown<len(self.availableCSVs)) else 0

  def __init__(self, dispRef, frameSize):
    super(DownloadCSV, self).__init__(dispRef, frameSize)
    offset = 30

    self.start = 0
    self.shown = 8
    self.visible = []
    self.client = client.Client(self.dispRef.mapDir, self.dispRef.imageDir)
    self.availableCSVs = self.client.getList("sorted")

    (cx, cy) = (self.frameWidth / 2.0, self.frameHeight / 2.0)
    objs = [shapes.Texture(cx, cy, "background.png"),
            buttons.TexturedButton(offset, self.frameHeight - offset,
              DownloadCSV.HOME, "home.png")]

    if(len(self.availableCSVs) > self.shown):
      objs += [buttons.TriangleButton(self.frameWidth - 4*offset, cy + 4*offset,
                ((0, 50), (-25, 0), (25, 0)), DownloadCSV.DOWN,""),
               buttons.TriangleButton(self.frameWidth - 4*offset, cy - 5*offset,
              ((0, -50), (-25, 0), (25, 0)), DownloadCSV.UP,"")]

    self.menu = menu.Menu(self.dispRef, self.frameSize, objs)
