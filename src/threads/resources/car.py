from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

from src.threads.resources import objects

class Car(object):
  def __init__(self, world, collisionSpace):
    self.world = world
    self.collisionSpace = collisionSpace

    self.wheelRadius = 1
    self.wheelHeight = 0.5
    self.bodyMass = 1.0
    self.wheelMass = 0.05*100
    self.deceleration = 0.001

    self.wheelSpeed = 0
    self.speedCutOff = 10

    #                      l, w, h
    self.bodyDimensions = (5.0, 4.0, 3.0)

    self.wheelColor = (0, 0, .5)
    self.carBodyColor = (.5, 0, 0)

    self.wheels = []
    self.carBody = None
    self.createCar()

  def rotateBody(self, body, (c, s, t), (x, y, z)):
    rotMatrix = [0] * 9
    rotMatrix[0] = t*(x**2) + c
    rotMatrix[1] = t*x*y - s*z
    rotMatrix[2] = t*x*z + s*y
    rotMatrix[3] = t*x*y + s*z
    rotMatrix[4] = t*(y**2) + c
    rotMatrix[5] = t*y*z - s*x
    rotMatrix[6] = t*x*z - s*x
    rotMatrix[7] = t*y*x + s*x
    rotMatrix[8] = t*(z**2) + c
    body.setRotation(rotMatrix)


  def createWheel(self, x, y, z, front = False):
    body = ode.Body(self.world)

    M = ode.Mass()
    M.setCylinderTotal(self.wheelMass, 1, self.wheelRadius, self.wheelHeight)
    M.mass = self.wheelMass

    body.setMass(M)
    body.setPosition((x, y, z))
    self.rotateBody(body, (1, 0, 0), (1, 0, 0))

    geom=ode.GeomCylinder(self.collisionSpace,self.wheelRadius,self.wheelHeight)
    geom.setBody(body)

    return (body, geom, front)

  def createBody(self, x, y, z):
    body = ode.Body(self.world)
    
    M = ode.Mass()
    (l, w, h) = self.bodyDimensions
    M.setBoxTotal(self.bodyMass, l, w, h)
    M.mass = self.bodyMass
    
    body.setMass(M)
    body.setPosition((x, y, z))
    
    geom = ode.GeomBox(self.collisionSpace, self.bodyDimensions)
    geom.setBody(body)
    return (body, geom)

  def createCar(self):
    for wheel in xrange(4):
      self.wheels += [self.createWheel(0, wheel - 2 , 10 + 5*wheel)]

    self.carBody = self.createBody(0, 0, 5)

  def drawWheels(self):
    slices = 20
    for (body, geom, front) in self.wheels:
      (r, h) = (self.wheelRadius, self.wheelHeight)
      objects.Cylinder(body.getPosition(), r, h, geom.getRotation(),
                         self.wheelColor).draw()

  def drawBody(self):
    (body, geom) = self.carBody
    (l, w, h) = self.bodyDimensions
    objects.Box(body.getPosition(), self.bodyDimensions, geom.getRotation(),
                  self.carBodyColor).draw()
 
  def drawCar(self):
    self.setWheelSpeed(self.wheelSpeed - self.deceleration)
    self.drawBody()
    self.drawWheels()

  def createJoints(self):
    pass

  def changePosition(self, dx, dy, dz):
    for (body, _, _) in self.wheels:
      (x, y, z) = body.getPosition()
      body.setPosition((x + dx, y + dy, z + dz))

    (body, _) = self.carBody
    body.setPosition((x + dx, y + dy, z + dz)) 

  def setWheelSpeed(self, speed):
    self.wheelSpeed = min(self.speedCutOff, speed)
    self.wheelSpeed = max(0, self.wheelSpeed)

  def setFrontWheelTurn(self, degrees):
    self.wheelTurn = degrees
