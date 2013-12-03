from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

class Object(object):
  def __init__(self, x, y, z, color):
    self.x = x
    self.y = y
    self.z = z
    self.color = color

  def applyTransform(self, x, y, z, rotation):
    trans = [0.0] * 16
    trans[ 0] = rotation[0]
    trans[ 1] = rotation[3]
    trans[ 2] = rotation[6]
    trans[ 3] = 0
    trans[ 4] = rotation[1]
    trans[ 5] = rotation[4]
    trans[ 6] = rotation[7]
    trans[ 7] = 0
    trans[ 8] = rotation[2]
    trans[ 9] = rotation[5]
    trans[10] = rotation[8]
    trans[11] = 0
    trans[12] = x
    trans[13] = y
    trans[14] = z
    trans[15] = 1
    glMultMatrixf(trans)

  def draw(self): pass

class Box(Object):
  def __init__(self, (x, y, z), (lx, ly, lz), rotation, color, 
                 borderColor = None, borderWidth = 5):
    super(Box, self).__init__(x, y, z, color)
    self.lx = lx
    self.ly = ly
    self.lz = lz
    self.rotation = rotation
    self.borderColor = borderColor
    self.borderWidth = borderWidth

  def createFace(self, x, y, z, used):
    (dx, dy, dz) = used
    signs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    verts = []
    if(dz == 0):
      verts = map(lambda (s1, s2) : (s1*x, s2*y, z), signs)
    elif(dy == 0):
      verts = map(lambda (s1, s2) : (s1*x, y, s2*z), signs)
    elif(dx == 0):
      verts = map(lambda (s1, s2) : (x, s1*y, s2*z), signs)
      
    for point in verts:
      glVertex3f(*point)

  def createVerts(self):
    dx = self.lx / 2.0
    dy = self.ly / 2.0
    dz = self.lz / 2.0

    for dir in [-dz, dz]:
      used = (1, 1, 0)
      self.createFace(dx, dy, dir, used)

    for dir in [-dy, dy]:
      used = (1, 0, 1)
      self.createFace(dx, dir, dz, used)

    for dir in [-dx, dx]:
      used = (0, 1, 1)
      self.createFace(dir, dy, dz, used)

  def createLineVerts(self):
    dx = self.lx / 2.0
    dy = self.ly / 2.0
    dz = self.lz / 2.0

    for dir in [-dz, dz]:
      used = (1, 1, 0)
      glBegin(GL_LINE_LOOP)
      self.createFace(dx, dy, dir, used)
      glEnd()

    glBegin(GL_LINES)
    glVertex3f(dx, dy, -dz)
    glVertex3f(dx, dy, dz)
    glVertex3f(dx, -dy, -dz)
    glVertex3f(dx, -dy, dz)
    glVertex3f(-dx, -dy, -dz)
    glVertex3f(-dx, -dy, dz)
    glVertex3f(-dx, dy, -dz)
    glVertex3f(-dx, dy, dz)
    glEnd()

  def drawBox(self):
    glColor(*self.color)
    glBegin(GL_QUADS)
    self.createVerts()
    glEnd()

  def drawBorders(self):
    glColor(*self.borderColor)
    glLineWidth(self.borderWidth)
    self.createLineVerts()

  def draw(self):
    glPushMatrix()
    self.applyTransform(self.x, self.y, self.z, self.rotation)
    self.drawBox()
    if(self.borderColor is not None): self.drawBorders()
    glPopMatrix()

class Cylinder(Object):
  def __init__(self, (x, y, z), r, h, rotation, color, borderColor = None, 
                 borderWidth = 5, fidelity = None):
    super(Cylinder, self).__init__(x, y, z, color)
    self.radius = r
    self.height = h
    self.rotation = rotation
    self.borderColor = (0, 0, 0)#None
    self.borderWidth = borderWidth

    if(fidelity is None):
      # Seems too be good radius to fidelity function
      self.fidelity = int(10 + r**(1/1.5))
    else:
      self.fidelity = fidelity

  def createCapBorder(self, zOff):
    for num in xrange(self.fidelity):
      piSlice = num * (2*math.pi/self.fidelity)
      (x, y) = (self.radius * math.cos(piSlice),
                self.radius * math.sin(piSlice))
      glVertex3f(x, y, zOff)

  def drawBorders(self):
    glColor(*self.borderColor)
    glLineWidth(self.borderWidth)
    glBegin(GL_LINE_LOOP)
    self.createCapBorder(-self.height / 2.0)
    glEnd()
    glBegin(GL_LINE_LOOP)
    self.createCapBorder(self.height / 2.0)
    glEnd()

    glBegin(GL_LINES)
    for num in xrange(self.fidelity):
      piSlice = num * (2*math.pi/self.fidelity)
      (x, y) = (self.radius * math.cos(piSlice),
                self.radius * math.sin(piSlice))
      glVertex3f(x, y, -self.height / 2.0)
      glVertex3f(x, y, self.height / 2.0)
    glEnd()

  def createCap(self, zOff):
    for num in xrange(self.fidelity):
      piSlice = num * (2*math.pi/self.fidelity)
      nextSlice = (num + 1) * (2*math.pi/self.fidelity)
      (x1, y1) = (self.radius * math.cos(piSlice),
                  self.radius * math.sin(piSlice))
      (x2, y2) = (self.radius * math.cos(nextSlice),
                  self.radius * math.sin(nextSlice))
      glVertex3f(x1, y1, zOff)
      glVertex3f(0, 0, zOff)
      glVertex3f(x2, y2, zOff)

  def drawCaps(self):
    glBegin(GL_TRIANGLES)
    self.createCap(-self.height / 2.0)
    self.createCap(self.height / 2.0)
    glEnd()

  def drawHoop(self):
    glBegin(GL_QUADS)
    for num in xrange(self.fidelity + 1):
      piSlice = num * (2*math.pi/self.fidelity)
      nextSlice = (num + 1) * (2*math.pi/self.fidelity)
      (x1, y1) = (self.radius * math.cos(piSlice),
                  self.radius * math.sin(piSlice))
      (x2, y2) = (self.radius * math.cos(nextSlice),
                  self.radius * math.sin(nextSlice))
      glVertex3f(x1, y1, -self.height / 2.0)
      glVertex3f(x2, y2, -self.height / 2.0)
      glVertex3f(x2, y2, self.height / 2.0)
      glVertex3f(x1, y1, self.height / 2.0)
    glEnd()

  def drawCylinder(self):
    glColor(*self.color)
    self.drawHoop()
    self.drawCaps()

  def draw(self):
    glPushMatrix()
    self.applyTransform(self.x, self.y, self.z, self.rotation)
    self.drawCylinder()
    if(self.borderColor is not None): self.drawBorders()
    glPopMatrix()  
