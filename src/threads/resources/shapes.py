from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy
import Image
import math

class Shape2D(object):
  def __init__(self, x, y, color):
    self.x = x
    self.y = y
    self.color = color

  def draw(self): pass

class Rectangle(Shape2D):
  def __init__(self, x, y, height, width, color, spin = 0, borderColor = None,
               borderWidth = 1):
    self.height = height
    self.width = width
    self.spin = spin
    self.borderColor = borderColor
    self.borderWidth = borderWidth
    super(Rectangle, self).__init__(x, y, color)

  def drawBorder(self):
    glColor(*self.borderColor)
    glLineWidth(self.borderWidth)
    glBegin(GL_LINES)

    glVertex2f(-self.width/2.0 - self.borderWidth/2.0, -self.height/2.0)
    glVertex2f(self.width/2.0 + self.borderWidth/2.0, -self.height/2.0)

    glVertex2f(-self.width/2.0 - self.borderWidth/2.0, self.height/2.0)
    glVertex2f(self.width/2.0 + self.borderWidth/2.0, self.height/2.0)

    glVertex2f(self.width/2.0, -self.height/2.0)
    glVertex2f(self.width/2.0, self.height/2.0)

    glVertex2f(-self.width/2.0, -self.height/2.0)
    glVertex2f(-self.width/2.0, self.height/2.0)

    glEnd()

  def drawFill(self):
    glColor(*self.color)
    glBegin(GL_QUADS)
    glVertex2f(-self.width/2.0, -self.height/2.0)
    glVertex2f(self.width/2.0, -self.height/2.0)
    glVertex2f(self.width/2.0, self.height/2.0)
    glVertex2f(-self.width/2.0, self.height/2.0)
    glEnd()

  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, 0)
    glRotate(self.spin, 0, 0, 1)
    self.drawFill()
    if(self.borderColor is not None): self.drawBorder()
    glPopMatrix()

class Circle(Shape2D):
  def __init__(self, x, y, radius, color, spin = 0, borderColor = None,
               borderWidth = 1, fidelity = None):
    self.radius = radius
    self.spin = spin
    self.borderColor = borderColor
    self.borderWidth = borderWidth

    if(fidelity is None):
      # Seems too be good radius to fidelity function
      self.fidelity = int(4 + radius**(1/1.5))
    else:
      self.fidelity = fidelity

    super(Circle, self).__init__(x, y, color)

  def createBorderVerts(self):
    for num in xrange(self.fidelity):
      piSlice = num * (2*math.pi/self.fidelity)
      (x, y) = (self.radius * math.cos(piSlice),
                self.radius * math.sin(piSlice))
      glVertex2f(x, y)

  def drawBorder(self):
    glColor(*self.borderColor)
    glLineWidth(self.borderWidth)
    glBegin(GL_LINE_LOOP)
    self.createBorderVerts()
    glEnd()

  def createFill(self):
    for num in xrange(self.fidelity):
      piSlice = num * (2*math.pi/self.fidelity)
      nextSlice = (num + 1) * (2*math.pi/self.fidelity)
      (x1, y1) = (self.radius * math.cos(piSlice),
                  self.radius * math.sin(piSlice))
      (x2, y2) = (self.radius * math.cos(nextSlice),
                  self.radius * math.sin(nextSlice))
      glVertex2f(x1, y1)
      glVertex2f(0, 0)
      glVertex2f(x2, y2)

  def drawFill(self):
    glColor(*self.color)
    glBegin(GL_TRIANGLES)
    self.createFill()
    glEnd()

  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, 0)
    glRotate(self.spin, 0, 0, 1)
    self.drawFill()
    if(self.borderColor is not None): self.drawBorder()
    glPopMatrix()

class Triangle(Shape2D):
  def __init__(self, x, y, verts, color, spin = 0, borderColor = None, 
                 borderWidth = 1):
    self.verts = verts
    self.spin = spin
    self.borderColor = borderColor
    self.borderWidth = borderWidth
    super(Triangle, self).__init__(x, y, color)

  def createVerts(self):
    for (x, y) in sorted(self.verts):
      glVertex2f(x, y)

  def midpoint(self, (x1, y1), (x2, y2)):
    return ((x2-x1)/2.0, (y2-y1)/2.0)

  def drawPoints(self):
    indexes = range(len(self.verts))
    for index in indexes:
      nonPicked = filter(lambda x : x != index, indexes)
      temp = []
      for newIndex in nonPicked:
        temp += [self.verts[newIndex]]

      (mx, my) = self.midpoint(*temp)

  def drawBorder(self):
    glColor(*self.borderColor)
    glLineWidth(self.borderWidth)
    glBegin(GL_LINE_LOOP)
    self.createVerts()
    glEnd()
    self.drawPoints()

  def drawFill(self):
    glColor(*self.color)
    glBegin(GL_TRIANGLES)
    self.createVerts()
    glEnd()

  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, 0) 
    glRotate(self.spin, 0, 0, 1)
    self.drawFill()
    if(self.borderColor is not None): self.drawBorder()
    glPopMatrix()

class Texture(Shape2D):
  def __init__(self, x, y, path, spin = 0, borderColor = None,
               borderWidth = 1):
    self.spin = spin
    self.borderColor = borderColor
    self.borderWidth = borderWidth
    
    self.loadImage(path)
    super(Texture, self).__init__(x, y, (0, 0, 0))

  def loadImage(self, path):
    self.image = Image.open(path)
    (self.width, self.height) = self.image.size

  def loadTexture(self):
    try:
      data = self.image.tostring("raw", "RGBA", 0, -1)
    except SystemError:
      data = self.image.tostring("raw", "RGBX", 0, -1)

    # generate a texture ID
    ID = glGenTextures(1)
    # make it current
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # copy the texture into the current texture ID
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA,
                   GL_UNSIGNED_BYTE, data)
    # return the ID for use
    return ID

  def setupTexture(self , ID):
    # texture-mode setup, was global in original
#    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # re-select our texture, could use other generated textures
    # if we had generated them earlier...
    glBindTexture(GL_TEXTURE_2D, ID)   # 2d texture (x and y size

  def drawBorder(self):
    glColor(*self.borderColor)
    glLineWidth(self.borderWidth)
    glBegin(GL_LINES)

    glVertex2f(-self.width/2.0 - self.borderWidth/2.0, -self.height/2.0)
    glVertex2f(self.width/2.0 + self.borderWidth/2.0, -self.height/2.0)

    glVertex2f(-self.width/2.0 - self.borderWidth/2.0, self.height/2.0)
    glVertex2f(self.width/2.0 + self.borderWidth/2.0, self.height/2.0)

    glVertex2f(self.width/2.0, -self.height/2.0)
    glVertex2f(self.width/2.0, self.height/2.0)

    glVertex2f(-self.width/2.0, -self.height/2.0)
    glVertex2f(-self.width/2.0, self.height/2.0)

    glEnd()

  def drawFill(self):
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE) #GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
 
    glEnable(GL_TEXTURE_2D)
    surface = self.loadTexture()
    self.setupTexture(surface)
    glBindTexture(GL_TEXTURE_2D, surface)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 1.0)
    glVertex2f(-self.width/2.0, -self.height/2.0)

    glTexCoord2f(1.0, 1.0)
    glVertex2f(self.width/2.0, -self.height/2.0)

    glTexCoord2f(1.0, 0)
    glVertex2f(self.width/2.0, self.height/2.0)

    glTexCoord2f(0, 0)
    glVertex2f(-self.width/2.0, self.height/2.0)

    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_TEXTURE_2D)
    #glPushMatrix()
    #glDisable(GL_BLEND)
  
  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, 0)
    glRotate(self.spin, 0, 0, 1)
    self.drawFill()
    if(self.borderColor is not None): self.drawBorder()
    glPopMatrix()
