from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.threads.resources import shapes

class Button(object):
  def __init__(self, x, y, ref):
    self.x = x
    self.y = y
    self.ref = ref

    self.fill = (1.0, 1.0, 1.0)
    self.borderColor = (0.0, 0.0, 0.0)
    self.borderWidth = 3

  def setBorder(self, color, width):
    self.borderColor = color
    self.borderWidth = width

  def draw(self): pass
  def registerEvent(self, mouseButton, state, x, y): pass

class RectangleButton(Button):
  def __init__(self, x, y, height, width, ref, text):
    self.text = text
    self.height = height
    self.width = width
    super(RectangleButton, self).__init__(x, y, ref)
    self.rectangle = shapes.Rectangle(x, y, height, width, self.fill, 0,
                                 self.borderColor, self.borderWidth)

  def draw(self):
    self.rectangle.draw()

  def registerEvent(self, mouseButton, state, x, y, 
		    desiredState = GLUT_DOWN, 
                    desiredButton = GLUT_LEFT_BUTTON):
    dx = abs(self.x - x)
    dy = abs(self.y - y)
    return ((dx <= self.width/2.0) and (dy <= self.height/2.0) and 
            (state == desiredState) and (mouseButton == desiredButton))

class CircleButton(Button):
  def __init__(self, x, y, radius, ref, text):
    self.text = text
    self.radius = radius
    super(CircleButton, self).__init__(x, y, ref)
    self.circle = shapes.Circle(x, y, radius, self.fill, 0, self.borderColor, 
                           self.borderWidth)

  def draw(self):
    self.circle.draw()

  def registerEvent(self, mouseButton, state, x, y, 
		    desiredState = GLUT_DOWN, 
                    desiredButton = GLUT_LEFT_BUTTON):
    dx = abs(self.x - x)
    dy = abs(self.y - y)
    return ((dx**2 + dy**2 <= self.radius) and (state == desiredState) and
            (mouseButton == desiredButton))

class TriangleButton(Button):
  def __init__(self, x, y, verts, ref, text):
    self.text = text
    self.verts = verts
    super(TriangleButton, self).__init__(x, y, ref)
    self.triangle = shapes.Triangle(x, y, verts, self.fill, 0, self.borderColor,
                               self.borderWidth)

  def draw(self):
    self.triangle.draw()

  def getSlope(self, (x1, y1), (x2, y2)):
    dx = (x2 - x1)
    dy = (y2 - y1)

    if(dx == 0):
      return None
    return float(dy)/dx

  def genLineEq(self, (x1, y1), (x2, y2)):
    m = self.getSlope((x1, y1), (x2, y2))
    if(m is None): return None
    return lambda x : m*(x - x1) + y1

  def registerEvent(self, mouseButton, state, x, y,
                    desiredState = GLUT_DOWN,
                    desiredButton = GLUT_LEFT_BUTTON):
    dx = abs(self.x - x)
    dy = abs(self.y - y)
    (minX, maxX) = (min(self.verts)[0] + self.x, max(self.verts)[0] + self.x)
    if(not(minX <= self.x <= maxX)): return False

    sortedVerts = map(lambda (x, y):(x + self.x, y + self.y),sorted(self.verts))

    indexes = range(len(sortedVerts))
    for index in indexes:
      nonPicked = filter(lambda x : x != index, indexes)
      
      temp = []
      for newIndex in nonPicked:
        temp += [sortedVerts[newIndex]]

      f = self.genLineEq(*temp)

      if(f is not None):
        (vx, vy) = sortedVerts[index]
        if(vy < f(vx)):
          if(y > f(x)): return False
        elif(vy > f(vx)):
          if(y < f(x)): return False

    return True
        
class TexturedButton(RectangleButton):
  def __init__(self, x, y, ref, texturePath):
    self.x = x
    self.y = y
    self.texturePath = texturePath
    self.borderColor = None #(0, 0, 0)
    self.borderWidth = 2

    self.setTexture(texturePath)
    super(TexturedButton, self).__init__(x, y, self.texture.height, 
                                           self.texture.width, ref, "")

  def draw(self):
    self.texture.draw()

  def setTexture(self, path):
    self.texture = shapes.Texture(self.x, self.y, path, 0, self.borderColor,
                                    self.borderWidth)
    self.height = self.texture.height
    self.width = self.texture.width
