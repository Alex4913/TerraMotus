from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ode

import math

from src.threads.resources import objects

class Car(object):
  acc = 0.5

  def __init__(self, world, collisionSpace):
    self.world = world
    self.collisionSpace = collisionSpace
    self.jointGroup = 0

    self.wheelRadius = 3
    self.wheelHeight = 0.65
    self.bodyMass = 15
    self.wheelMass = 1
    self.deceleration = 0.01

    self.wheelSpeed = 0
    self.wheelTurn = 0
    self.steerRange = .42
    
    self.maxForce = 100
    self.speedCutOff = 10000
    self.rescueOffset = 5

    #                      l, w, h
    self.bodyDimensions = (12, 6, 6)

    self.wheelColor = (0, 0, .5)
    self.carBodyColor = (.5, 0, 0)

    self.wheels = []
    self.carBody = None

  def quatFromAxisAndAngle(self, ax, ay, az, angle):
    quaternion = [0.0] * 4
    l = ax**2 + ay**2 + az**2
    if(l > 0.0):
      angle *= 0.5
      quaternion[0] = math.cos(angle)
      l = math.sin(angle) * 1.0/(l**0.5)
      quaternion[1] = ax * l
      quaternion[2] = ay * l
      quaternion[3] = az * l
    else:
      quaternion = [1.0, 0, 0, 0]

    return quaternion

  def quatToRotMatrix(self, quaternion):
    rot = [0.0] * 9
    qp1 = 2 * quaternion[1]**2
    qp2 = 2 * quaternion[2]**2
    qp3 = 2 * quaternion[3]**2

    rot[0] = 1 - qp2 - qp3
    rot[1] = 2 * (quaternion[1]*quaternion[2] - quaternion[0]*quaternion[3])
    rot[2] = 2 * (quaternion[1]*quaternion[3] - quaternion[0]*quaternion[2])

    rot[3] = 2 * (quaternion[1]*quaternion[2] - quaternion[0]*quaternion[3])
    rot[4] = 1 - qp1 - qp3
    rot[5] = 2 * (quaternion[2]*quaternion[3] - quaternion[0]*quaternion[1]) 

    rot[6] = 2 * (quaternion[1]*quaternion[3] - quaternion[0]*quaternion[2])
    rot[7] = 2 * (quaternion[2]*quaternion[3] - quaternion[0]*quaternion[1])
    rot[8] = 1 - qp1 - qp2

    return rot

  def rotMatrixFromAxisAndAngle(self, ax, ay, az, angle):
    quaternion = quatFromAxisAndAngle(ax, ay, az, angle)
    return quatToRotMatrix(quaternion)

  def createWheel(self, x, y, z, front = False):
    body = ode.Body(self.world)
    body.setQuaternion(self.quatFromAxisAndAngle(1, 0, 0, math.pi * 0.5))

    M = ode.Mass()
    M.setCylinderTotal(self.wheelMass, 1, self.wheelRadius, self.wheelHeight)
    M.mass = self.wheelMass

    body.setMass(M)
    body.setPosition((x, y, z))

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

  def createCar(self, cx = 0, cy = 0, cz = 5):
    (l, w, h) = self.bodyDimensions
    (hl, hw, hh) = (l/2.0, 1.3*w/2.0, h/2.0)

    self.wheels = [self.createWheel(cx + hw, cy + hl, cz - hh, True),
                   self.createWheel(cx - hw, cy + hl, cz - hh, False),
                   self.createWheel(cx + hw, cy - hl, cz - hh, True),
                   self.createWheel(cx - hw, cy - hl, cz - hh, False)]

    self.carBody = self.createBody(cx, cy, cz)
    self.createJoints()

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
    self.drawBody()
    self.drawWheels()

  def createJoints(self):
    self.frontJoints = []
    self.backJoints = []
    self.jointGroup = ode.JointGroup()
    for wheel in self.wheels:
      joint = ode.Hinge2Joint(self.world, self.jointGroup)
      (cBody, _) = self.carBody
      (wBody, _, front) = wheel
      joint.attach(cBody, wBody)
      joint.setAnchor(wBody.getPosition())
      joint.setAxis1((0, 0, 1))
      joint.setAxis2((0, 1, 0))
      if(front): self.frontJoints += [joint]
      else: self.backJoints += [joint]

    suspensionERP = 5
    suspensionCFM = 0.2

    for joint in xrange(len(self.frontJoints)):
      self.frontJoints[joint].setParam(ode.ParamSuspensionERP, suspensionERP)
      self.frontJoints[joint].setParam(ode.ParamSuspensionCFM, suspensionCFM)

    for joint in xrange(len(self.backJoints)):
      self.backJoints[joint].setParam(ode.ParamSuspensionERP, suspensionERP)
      self.backJoints[joint].setParam(ode.ParamSuspensionCFM, suspensionCFM)

    for joint in xrange(len(self.backJoints)):
      self.backJoints[joint].setParam(ode.ParamLoStop, 0)
      self.backJoints[joint].setParam(ode.ParamHiStop, 0)

  def steer(self):
    for joint in xrange(len(self.frontJoints)):
      error = self.wheelTurn - self.frontJoints[joint].getAngle1()
      error = max(-self.steerRange, error)
      error = min(self.steerRange, error)

      self.frontJoints[joint].setParam(ode.ParamVel, 10*error)
      self.frontJoints[joint].setParam(ode.ParamFMax, self.maxForce)
      self.frontJoints[joint].setParam(ode.ParamLoStop, -self.steerRange)
      self.frontJoints[joint].setParam(ode.ParamHiStop, self.steerRange)
      self.frontJoints[joint].setParam(ode.ParamFudgeFactor, 0.1)

  def motor(self):
    for jointGroup in [self.frontJoints, self.backJoints]:
      for joint in xrange(len(jointGroup)):
        jointGroup[joint].setParam(ode.ParamVel2, -self.wheelSpeed)
        jointGroup[joint].setParam(ode.ParamFMax2, self.maxForce) 

  def simulate(self):
    if(self.wheelSpeed > 0):
      self.setWheelSpeed(self.wheelSpeed - self.deceleration)
    elif(self.wheelSpeed < 0):
      self.setWheelSpeed(self.wheelSpeed + self.deceleration)

    self.motor()
    self.steer()

  def getPos(self):
    (body, _) = self.carBody
    return body.getPosition()

  def getRPY(self):
    (body, _) = self.carBody
    R = body.getRotation()
    roll  = math.atan2(R[7], R[8])
    pitch = math.asin(-R[6])
    yaw   = math.atan2(R[3], R[0])
    return (roll, pitch, yaw)

  def changePosition(self, dx, dy, dz):
    for (body, _, _) in self.wheels:
      (x, y, z) = body.getPosition()
      body.setPosition((x + dx, y + dy, z + dz))

    (body, _) = self.carBody
    body.setPosition((x + dx, y + dy, z + dz)) 

  def resetPos(self):
    (x, y, z) = self.getPos()
    self.createCar(x, y, z + self.rescueOffset) 

  def setWheelSpeed(self, speed):
    self.wheelSpeed = min(self.speedCutOff, speed)
    self.wheelSpeed = max(-self.speedCutOff, self.wheelSpeed)

  def accelerate(self, acc):
    self.setWheelSpeed(self.wheelSpeed + acc)

  def setFrontWheelTurn(self, val):
    self.wheelTurn += val
    self.wheelTurn = max(-self.steerRange, self.wheelTurn)
    self.wheelTurn = min(self.steerRange, self.wheelTurn)
