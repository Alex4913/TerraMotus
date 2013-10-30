import copy

class Point(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __eq__(self, other):
    return ((self.x == other.x) and
            (self.y == other.y) and
            (self.z == other.z))

  def toOrderedPairs(self):
    return (self.x, self.y, self.z)

class Vector(object):
  def __init__(self, i, j, k):
    self.i = i
    self.j = j
    self.k = k

  def __eq__(self, other):
    return ((self.i == other.i) and
            (self.j == other.j) and
            (self.k == other.k))

class Triangle(object):
  def getVector(self, pt1, pt2):
    return Vector(pt2.x - pt1.x, pt2.y - pt1.y, pt2.z - pt1.z)
  
  def getCrossProduct(self, vec1, vec2):
    crossP = Vector(0, 0, 0)
    crossP.i =   (vec1.j + vec2.k) - (vec1.k + vec2.j)
    crossP.j = -((vec1.i + vec2.k) - (vec1.k + vec2.i))
    crossP.k =   (vec1.i + vec2.j) - (vec1.j + vec2.i)
  
    return crossP
  
  def toPoints(self):
    return (self.pt1, self.pt2, self.pt3)

  def __init__(self, pt1, pt2, pt3):
    (self.pt1, self.pt2, self.pt3) = sorted((pt1, pt2, pt3))
    self.vect1 = self.getVector(pt2, pt1)
    self.vect2 = self.getVector(pt2, pt3)
  
    self.normal = self.getCrossProduct(self.vect1, self.vect2)

  def __eq__(self, other):
    return self.normal == other.normal

class PlaneData(object):
  def getDotProduct(vec1, vec2):
    return (vec1.i * vec2.i) + (vec1.j * vec2.j) + (vec1.k * vec2.k)

  def getBounds(self):
    minVal = None
    maxVal = None
    for row in self.rawData:
      minVal = min(minVal, min(row)) if(minVal is not None) else min(row)
      maxVal = max(maxVal, max(row)) if(maxVal is not None) else max(row)

    return (minVal, maxVal)

  def getPoint(self, y, x):
    return Point(y, x, self.rawData[y][x])

  def setPoint(self, y, x, z):
    self.rawData[y][x] = z

    self.maxVal = max(self.maxVal, z)
    self.minVal = min(self.minVal, z)

    self.verts[(y * self.width) + x] = Point(y, x, z)

  def toVertices(self):
    if(self.verts is not None):
      return self.verts

    result = []
    for y in xrange(self.height):
      for x in xrange(self.width):
        result += [self.getPoint(y, x)]

    self.verts = result
    return result

  def toRawVertices(self):
    if(self.rawVertices != None):
      return self.rawVertices

    result = []
    for y in xrange(self.height):
      for x in xrange(self.width):
        result += [(y, x, self.getPoint(y, x).z)]

    self.rawVertices = result  
    return result

  def toTriangles(self):
    if(self.triangles is not None):
      return self.triangles

    triangles = []
    for point in xrange(len(self.verts)): 
      if((point % self.width < self.width - 1) and 
           (point / self.width < self.height - 1)):
        triangles += [Triangle(self.verts[point],
                               self.verts[point + self.width],
                               self.verts[point + 1])]

        triangles += [Triangle(self.verts[point + 1],
                               self.verts[point + self.width],
                               self.verts[point + self.width + 1])]

    self.triangles = triangles
    return triangles

  def toTriangleIndexes(self):
    if(self.triangleIndexes is not None):
      return self.odeTriangleIndexes

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

      flattenedAndConverted += [converted]

    self.vbo = flattenedAndConverted
    return flattenedAndConverted

  def __init__(self, depthData):
    self.rawData = depthData
    (self.height, self.width) = (len(depthData), len(depthData[0]))

    (self.minVal, self.maxVal) = self.getBounds()
    
    self.verts = None
    self.rawVertices = None
    self.triangles = None
    self.triangleIndexes = None
    self.vbo = None
