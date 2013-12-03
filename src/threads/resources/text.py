from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Character(object):
  def __init__(self, font, char, color, x, y):
    self.font = font
    self.char = char
    self.color = color
    self.x = x
    self.y = y

  def getSpacing(self):
    if(self.font == GLUT_BITMAP_8_BY_13):
      return (8 ,13)
    elif(self.font == GLUT_BITMAP_9_BY_15):
      return (9, 15)
    elif(self.font == GLUT_BITMAP_TIMES_ROMAN_10):
      return (10, 10)
    elif(self.font == GLUT_BITMAP_TIMES_ROMAN_24):
      return (24, 24)
    elif(self.font == GLUT_BITMAP_HELVETICA_10):
      return (10, 10)
    elif(self.font == GLUT_BITMAP_HELVETICA_12):
      return (12, 12)
    elif(self.font == GLUT_BITMAP_HELVETICA_18):
      return (18, 18)
    else:
      return (None, None)

  def draw(self):
    glPushMatrix()
    glTranslatef(self.x, self.y, 0)
    glRasterPos(0, 0, 0)
    glColor(*self.color)
    glutBitmapCharacter(self.font, ord(self.char))
    glPopMatrix()

class Text(Character):
  def __init__(self, font, text, color, x, y):
    self.font = font
    self.color = color
    self.x = x
    self.y = y

    (xOff, _) = self.getSpacing()
    self.width = (xOff * len(text))/2.0
    self.chars = []
    for char in xrange(len(text)):
      self.chars += [Character(self.font, text[char], self.color, 
                               self.x - self.width + xOff*char, self.y)]

  def draw(self):
    for char in self.chars:
      char.draw()

class TextBody(Text):
  def __init__(self, font, text, color, x, y):
    self.font = font
    self.color = color
    self.x = x
    self.y = y

    self.lines = text.split("\n")
    (_, yOff) = self.getSpacing()
    self.height = (yOff * len(self.lines))/2.0
    self.textLines = []
    for line in xrange(len(self.lines)):
      self.textLines += [Text(self.font, self.lines[line], self.color, self.x, 
                              self.y - self.height + yOff*line)]

  def draw(self):
    for line in self.textLines:
      line.draw()
