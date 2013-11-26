from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import time
import math

from src.threads.resources import car, buttons, menu
from src.threads.frames import frame

class Simulation(frame.Frame):
  # World Properties
  # A nice light blue
  skyColor = (0.0, 178.0/255.0, 255.0/255.0, 255.0/255.0)

  # White with no opacity
  defaultColor = (1.0, 1.0, 1.0)

  HOME = 1
  UPLOAD = 2

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
    pass

  def draw(self):
    self.preGL()
    
    self.drawTriMesh()
    self.drawCar()
    self.menu.draw()

  def timerFired(self, value):
    if(not(self.dataThread.graphicsQueue.empty())):
      self.dataPlane = self.dataThread.graphicsQueue.get()

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.menu.mouse(mouseButton, buttonState, x, y)
      self.buttonsPressed = map(lambda x : x.ref, self.menu.buttonEvents)

  def keyboard(self, key, x, y):
    self.eyeRoll += -(key == "d")/2.0 + (key == "a")/2.0
    self.eyePitch += -(key == "s")/2.0 + (key == "w")/2.0
    self.eyeYaw += -(key == "z")/10.0 + (key == "x")/10.0
    if(key == "p"): print self.eyeX, self.eyeY, self.eyeZ

  def specialKeys(self, key, x, y):
    self.eyeX += -(key == GLUT_KEY_DOWN) + (key == GLUT_KEY_UP)
    self.eyeY += (key == GLUT_KEY_LEFT) + -(key == GLUT_KEY_RIGHT)
    self.eyeZ += -(key == GLUT_KEY_PAGE_DOWN) + (key == GLUT_KEY_PAGE_UP)

  def pause(self, state = True):
    self.paused = state
    self.physicsThread.paused = self.paused

  def __init__(self, frameSize, dataThread, physicsThread):
    super(Simulation, self).__init__(frameSize)
    self.dataThread = dataThread
    self.physicsThread = physicsThread
    self.dataPlane = None
    self.car = None
    self.update = True
    self.planePresent = True
    self.paused = True

    if(not(self.dataThread.graphicsQueue.empty())):
      self.dataPlane = self.dataThread.graphicsQueue.get()
    else:
      self.planePresent = False

    self.genVBOs()
    self.eyeX = -1.5 * self.dataPlane.width
    self.eyeY = 0
    self.eyeZ = self.dataPlane.minVal + 10
    self.eyeRoll = self.eyePitch = self.eyeYaw = 0

    # Pic-widths = 50x50
    b = buttons.TexturedButton(30, self.height - 30, Simulation.HOME,"home.png")
    b2= buttons.TexturedButton(80,self.height-30,Simulation.UPLOAD,"upload.png")
    self.menu = menu.Menu(self.frameSize, [b, b2])
    self.buttonsPressed = []
