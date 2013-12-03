from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import time
import math

from src.threads.resources import car, buttons, menu
from src.threads.frames import frame, menus
from src.threads import converter, uploadThread, engine

class Simulation(frame.Frame):
  # World Properties
  # A nice light blue
  skyColor = (0.0, 178.0/255.0, 255.0/255.0, 255.0/255.0)

  # White with no opacity
  defaultColor = (1.0, 1.0, 1.0)

  # In seconds
  planeUpdateDelay = 2

  HOME = 1
  UPLOAD = 2
  PAUSE = 3
  PAUSE_TEX = "pause.png"
  UNPAUSE_TEX = "unpause.png"

  def preGL(self):
    glEnable(GL_DEPTH_TEST)
    glClearColor(*Simulation.skyColor)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(*Simulation.defaultColor)
    glLoadIdentity()
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Degree of FOV, width / height ratio, min dist, max dist
    gluPerspective(60, 1.5, 0.2, 1000)
    glMatrixMode(GL_MODELVIEW)
    self.setCamera(self.eyeX, self.eyeY, self.eyeZ,
                   self.eyeRoll, self.eyePitch, self.eyeYaw)

  def setCamera(self, x, y, z, roll, pitch, yaw):
    # Unit Circle
    lookX = math.cos(yaw) + x
    lookY = math.sin(yaw) + y

    gluLookAt (x, y, z, lookX, lookY, z, 0, 0, 1)
    glRotatef(roll, 1.0, 0, 0)
    glRotatef(pitch, 0, 1.0, 0)
  
  def heightToColor(self, val):
    valRange = self.dataPlane.maxVal - self.dataPlane.minVal
    valScale = 1.0
    if(valRange == 0): return [0.5 * valScale]*3

    return [(float(val - self.dataPlane.minVal) / valRange) * valScale] * 3

  def genVBOs(self):
    if(self.update == True):
      self.vbo = vbo.VBO(numpy.array(self.dataPlane.toVBO(), 'f'))

      colorRaw = []
      for (_, _, z) in self.dataPlane.toVBO():
        colorRaw += [self.heightToColor(z)]

      self.colorVBO = vbo.VBO(numpy.array(colorRaw, 'f'))
      self.update = False
 
  def drawTriMesh(self):
    self.genVBOs()
    glPushMatrix()
    glTranslatef(-self.dataPlane.width/2.0, -self.dataPlane.height/2.0, 0)

    try:
      glEnableClientState(GL_COLOR_ARRAY)
      self.colorVBO.bind()
      try:
        glColorPointer(3, GL_FLOAT, 0, self.colorVBO)
      except: pass
  
      glEnableClientState(GL_VERTEX_ARRAY)
      self.vbo.bind()

      try:
        glVertexPointer(3, GL_FLOAT, 0, self.vbo)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vbo))
        
      except:
        pass
      finally:
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        self.vbo.unbind()
        self.colorVBO.unbind()

    except:
      pass

    glPopMatrix()

  def drawCar(self):
    self.physicsThread.car.drawCar()

  def draw(self):
    lol = time.time()
    self.preGL()
    
    self.drawCar()
    self.drawTriMesh()
    if(self.upload):
      if(self.upThread is None):
        self.upThread = uploadThread.Worker(self.mapDir, self.dataPlane,
                                              self.uploadButton)
        self.upThread.start()
      else:
        if(self.upThread.done):
          self.upThread = None
          self.upload = False

    self.menu.draw()
    self.menu.postGL()

  def timerFired(self, value):
    if(time.time() - self.timeFromLastUpdate >= Simulation.planeUpdateDelay):
      if(not(self.dataSource.graphicsQueue.empty())):
        self.dataPlane = self.dataSource.graphicsQueue.get()
        self.update = True
        self.timeFromLastUpdate = time.time()
      self.physicsThread.update()

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)
      
      if(Simulation.HOME in self.buttonsPressed):
        self.pause(True)
        self.dispRef.currentFrame = menus.MainMenu(self.dispRef, self.frameSize)
      if(Simulation.UPLOAD in self.buttonsPressed):
        if(not(self.upload)):
          self.upload = True
      if(Simulation.PAUSE in self.buttonsPressed):
        self.pause(not(self.paused))
        if(self.paused):
          self.pauseButton.setTexture(Simulation.UNPAUSE_TEX)
        else:
          self.pauseButton.setTexture(Simulation.PAUSE_TEX)

  def keyboard(self, key, x, y):
    self.eyeRoll += -(key == "d") + (key == "a")
    self.eyePitch += -(key == "s") + (key == "w")
    self.eyeYaw += -(key == "z")/15.0 + (key == "x")/15.0
    if(key == "p"): print self.eyeX, self.eyeY, self.eyeZ

  def specialKeys(self, key, x, y):
    self.eyeX += -(key == GLUT_KEY_DOWN)*1.5 + (key == GLUT_KEY_UP)*1.5
    self.eyeY += (key == GLUT_KEY_LEFT)*1.5 + -(key == GLUT_KEY_RIGHT)*1.5
    self.eyeZ += -(key == GLUT_KEY_PAGE_DOWN)*1.5 +(key == GLUT_KEY_PAGE_UP)*1.5

  def pause(self, state = True):
    self.paused = state
    self.physicsThread.paused = self.paused

  def stop(self):
    try:
      self.physicsThread.stop()
    except: pass
    try:
      self.dataSource.terminate()
    except: pass

  def setup(self, dataSource):
    self.dataSource = converter.Converter(dataSource)
    self.dataSource.start()

    while(self.dataSource.graphicsQueue.empty()): pass

    self.physicsThread = engine.Engine(self.dataSource.physicsQueue)
    self.physicsThread.start()
       
    if(not(self.dataSource.graphicsQueue.empty())):
      self.dataPlane = self.dataSource.graphicsQueue.get()
    else:
      self.planePresent = False

    self.eyeX = -1.5 * self.dataPlane.width
    self.eyeY = 0
    self.eyeZ = self.dataPlane.minVal + 10
    self.eyeRoll = self.eyePitch = self.eyeYaw = 0
    
    self.setuped = True
    self.update = True
    self.timeFromLastUpdate = time.time()
    self.pause(False)

  def __init__(self, dispRef, frameSize, mapDir):
    super(Simulation, self).__init__(dispRef, frameSize)
    self.mapDir = mapDir
    self.dataPlane = None
    self.car = None
    self.update = True
    self.setuped = False
    self.planePresent = True
    self.paused = True
    self.upload = False
    self.upThread = None

    picWidth = 50
    offset = 30
    self.homeButton = buttons.TexturedButton(offset, self.frameHeight - offset, 
                                               Simulation.HOME, "home.png")
    self.uploadButton = buttons.TexturedButton(picWidth + offset, 
                                               self.frameHeight - offset,
                                               Simulation.UPLOAD, "upload3.png")
    self.pauseButton = buttons.TexturedButton(2*picWidth + offset,
                                               self.frameHeight - offset,
                                               Simulation.PAUSE, 
                                               Simulation.PAUSE_TEX)
    self.menu = menu.Menu(self.dispRef, self.frameSize, 
                          [self.homeButton,self.uploadButton,self.pauseButton])
    self.buttonsPressed = []
