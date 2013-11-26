import copy
import math

class Point(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __eq__(self, other):
    return ((self.x == other.x) and
            (self.y == other.y) and
            (self.z == other.z))

  def __str__(self):
    return "Point (%s, %s, %s)" % (str(self.x), str(self.y), str(self.z)) 

  def toOrderedPairs(self):
    return (self.x, self.y, self.z)

class Vector(object):
  def getMagnitude(self):
    return (self.i**2 + self.j**2 + self.k**2)**(0.5)

  def __init__(self, i, j, k):
    self.i = i
    self.j = j
    self.k = k
    self.magnitude = self.getMagnitude()

  def __str__(self):
    return "Vector <%s, %s, %s>" % (str(self.i), str(self.j), str(self.k))

  def __eq__(self, other):
    return ((self.i == other.i) and
            (self.j == other.j) and
            (self.k == other.k))

  def getDotProduct(self, other):
    return (self.i * other.i) + (self.j * other.j) + (self.k * other.k)

  def angleBetween(self, other):
    dotProd = self.getDotProduct(other)
    multMags = self.magnitude * other.magnitude
    return math.degrees(math.acos(round(dotProd / multMags, 10)))

class Triangle(object):
  def getVector(self, pt1, pt2):
    return Vector(pt2.x - pt1.x, pt2.y - pt1.y, pt2.z - pt1.z)
  
  def getCrossProduct(self, vec1, vec2):
    crossP = Vector((vec1.j + vec2.k) - (vec1.k + vec2.j),
                    -((vec1.i + vec2.k) - (vec1.k + vec2.i)),
                     (vec1.i + vec2.j) - (vec1.j + vec2.i))
  
    return crossP
  
  def toPoints(self):
    return (self.pt1, self.pt2, self.pt3)

  def __init__(self, pt1, pt2, pt3):
    (self.pt1, self.pt2, self.pt3) = sorted((pt1, pt2, pt3))
    self.vect1 = self.getVector(self.pt2, self.pt1)
    self.vect2 = self.getVector(self.pt2, self.pt3)
  
    self.normal = self.getCrossProduct(self.vect1, self.vect2)

  def __eq__(self, other):
    return self.normal == other.normal

class PlaneData(object):
  def getBounds(self):
    minVal = None
    maxVal = None
    for row in self.rawData:
      minVal = min(minVal, min(row)) if(minVal is not None) else min(row)
      maxVal = max(maxVal, max(row)) if(maxVal is not None) else max(row)

    self.minVal = minVal
    self.maxVal = maxVal
    return (minVal, maxVal)

  def getPoint(self, x, y):
    return Point(x, y, self.rawData[y][x])

  def setPoint(self, x, y, z):
    self.rawData[y][x] = z

    self.maxVal = max(self.maxVal, z)
    self.minVal = min(self.minVal, z)

    self.verts[(y * self.width) + x] = Point(x, y, z)

  def toVertices(self):
    if(self.verts is not None):
      return self.verts

    result = []
    for y in xrange(self.height):
      for x in xrange(self.width):
        result += [self.getPoint(x, y)]

    self.verts = result
    return result

  def toRawVertices(self):
    if(self.rawVertices != None):
      return self.rawVertices

    result = []
    for y in xrange(self.height):
      for x in xrange(self.width):
        result += [(y, x, self.getPoint(x, y).z)]

    self.rawVertices = result  
    return result

  def toTriangles(self):
    if(self.triangles is not None):
      return self.triangles

    if(self.verts is None):
      self.toVertices()

    triangles = []
    for row in xrange(self.height):
      temp = []
      for col in xrange(self.width):
        point = (row * self.width) + col
        if((point % self.width < self.width - 1) and 
             (point / self.width < self.height - 1)):
          temp += [Triangle(self.verts[point],
                              self.verts[point + self.width],
                              self.verts[point + 1])]

          temp += [Triangle(self.verts[point + 1],
                              self.verts[point + self.width],
                              self.verts[point + self.width + 1])]

      triangles += [temp]

    self.triangles = triangles
    return triangles

  def toTriangleIndexes(self):
    if(self.triangleIndexes is not None):
      return self.triangleIndexes

    verts = self.toVertices()
    (height, width) = (self.height, self.width)
    
    triangles = []
    for point in xrange(len(self.verts)):
      if((point % self.width < self.width - 1) and 
          (point / self.width < self.height - 1)): 
        triangles += [(point, point + self.width, point + 1)]
        triangles += [(point + 1, point + self.width, point + self.width + 1)]
    
    self.triangleIndexes = triangles
    return triangles

  def toVBO(self):
    if(self.vbo is not None):
      return self.vbo

    triangleIndexes = self.toTriangleIndexes()
    verts = self.toVertices()
    flattenedAndConverted = []
    for triset in triangleIndexes:
      converted = []
      for index in triset:
        converted += [verts[index].toOrderedPairs()]

      flattenedAndConverted += converted

    self.vbo = flattenedAndConverted
    return flattenedAndConverted

  def __init__(self, depthData, name = ""):
    self.rawData = depthData
    self.name = name
    (self.height, self.width) = (len(depthData), len(depthData[0]))

    (self.minVal, self.maxVal) = self.getBounds()
    
    self.verts = None
    self.rawVertices = None
    self.triangles = None
    self.triangleIndexes = None
    self.vbo = None

  def __repr__(self):
    name = "self.name='%s'" % self.name
    if(name != ""):
      return "%s(%s, %s)" % (PlaneData.__name__, str(self.rawData), name)
    else:
      return "%s(%s)" % (PlaneData.__name__, str(self.rawData))
