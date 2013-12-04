from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import time
import math

from src.threads.resources import car, buttons, menu
from src.threads.frames import frame, menus
from src.threads import converter, sources, uploadThread, engine

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
                   self.eyeRoll, self.eyePitch, self.eyeYaw, 30)

  def setCamera(self, x, y, z, roll, pitch, yaw, r = 1):
    # Unit Circle
    lookX = -r*math.cos(yaw) + x
    lookY = -r*math.sin(yaw) + y

    gluLookAt (lookX, lookY, z, x, y, z, 0, 0, 1)
    glRotatef(roll, 1.0, 0, 0)
    glRotatef(pitch, 0, 1.0, 0)
  
  def genVBOs(self):
    if(self.update == True):
      self.vbo = vbo.VBO(numpy.array(self.dataPlane.toVBO(), 'f'))
      self.colorVBO = vbo.VBO(numpy.array(self.dataPlane.toColorVBO(), 'f'))
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
    (x, y, z) = self.physicsThread.car.getPos()
    (self.eyeX, self.eyeY, self.eyeZ) = (x, y, z + 10)
    (r, p, y) = self.physicsThread.car.getRPY()
    self.eyeYaw = y

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
    (_, _, z) = self.physicsThread.car.getPos()
    if(z <= self.dataPlane.minVal):
      self.physicsThread.makeCar()

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
    if(key == "w"):
      self.physicsThread.car.accelerate(car.Car.acc)
    elif(key == "s"):
      self.physicsThread.car.accelerate(-car.Car.acc)
    elif(key == "a"):
      self.physicsThread.car.setFrontWheelTurn(-.25)
    elif(key == "d"):
      self.physicsThread.car.setFrontWheelTurn(.25)
    elif(key == " "):
      self.physicsThread.car.setWheelSpeed(0)
      self.physicsThread.car.setFrontWheelTurn(0)
      self.physicsThread.car.resetPos()
    elif(key == "r"):
      self.physicsThread.car.setWheelSpeed(0)
      self.physicsThread.car.setFrontWheelTurn(0)
      self.physicsThread.makeCar()

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
    self.dataSource = converter.Converter(dataSource, self.dispRef.mapDir)
    self.dataSource.start()

    while(self.dataSource.graphicsQueue.empty()): pass

    self.physicsThread = engine.Engine(self.dataSource.physicsQueue)
    self.physicsThread.start()
       
    if(not(self.dataSource.graphicsQueue.empty())):
      self.dataPlane = self.dataSource.graphicsQueue.get()
    else:
      self.planePresent = False
    if(isinstance(dataSource, sources.CSVSource)): pass
    self.dataSource.terminate()

    self.eyeX = -self.dataPlane.width/2.0
    self.eyeY = 0
    self.eyeZ = self.dataPlane.maxVal + 10
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
