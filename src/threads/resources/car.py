from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

class Car(object):
  def __init__(self, world, collisionSpace):
    self.world = world
    self.collisionSpace = collisionSpace

    self.wheelRadius = 1
    self.wheelHeight = 0.5
    self.bodyMass = 1.0
    self.wheelMass = 0.05
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

  def createWheel(self, x, y, z, front = False):
    body = ode.Body(self.world)

    M = ode.Mass()
    M.setSphereTotal(self.wheelMass, self.wheelRadius)
    M.mass = self.wheelMass

    body.setMass(M)
    body.setPosition((x, y, z))

    geom=ode.GeomSphere(self.collisionSpace,self.wheelRadius)
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
    for wheel in xrange(1):
      for j in xrange(1):
        self.wheels += [self.createWheel(wheel*2, j*2, 5)]
#    self.carBody = self.createBody(0, 0, 5)

  def setTransform(self, pos, R):
    trans = [0.0] * 16
    trans[ 0] = R[0] #0
    trans[ 1] = R[3] #3
    trans[ 2] = R[6] #6
    trans[ 3] = 0
    trans[ 4] = R[1] #1
    trans[ 5] = R[4] #4
    trans[ 6] = R[7] #7
    trans[ 7] = 0
    trans[ 8] = R[2] #2
    trans[ 9] = R[5] #5
    trans[10] = R[8] #8
    trans[11] = 0
    trans[12] = pos[0]
    trans[13] = pos[1]
    trans[14] = pos[2]
    trans[15] = 1
    glMultMatrixf(trans)

  def drawWheels(self):
    slices = 20
    for (body, geom, front) in self.wheels:
      (r, h) = (self.wheelRadius, self.wheelHeight)

      glPushMatrix()
      self.setTransform(body.getPosition(), geom.getRotation())
      glColor3f(*self.wheelColor)
      gluSphere(gluNewQuadric(), r, slices, slices) 
      glPopMatrix()

  def drawBody(self):
    (body, geom) = self.carBody
    glPushMatrix()
    self.setTransform(body.getPosition(), geom.getRotation())
    glColor3f(*self.carBodyColor)
    gluCylinder(gluNewQuadric(), 2, 2, 2, 20, 20) 
    glPopMatrix()
    
  def drawCar(self):
    self.setWheelSpeed(self.wheelSpeed - self.deceleration)
#    self.drawBody()
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
