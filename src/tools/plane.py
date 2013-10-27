import copy

class Point(object):
  (x, y, z) = (0, 0, 0)

  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __eq__(self, other):
    return ((self.x == other.x) and
            (self.y == other.y) and
            (self.z == other.z))

class Vector(object):
  (i, j, k) = (0, 0, 0)

  def __init__(self, i, j, k):
    self.i = i
    self.j = j
    self.k = k

  def __eq__(self, other):
    return ((self.i == other.i) and
            (self.j == other.j) and
            (self.k == other.k))

class Triangle(object):
  pt1 = None
  pt2 = None
  pt3 = None

  vect1 = None
  vect2 = None

  normal = None

  def getVector(pt1, pt2):
    return (pt2.x - pt1.x, pt2.y - pt1.y, pt2.z - pt1.z)
  
  def getCrossProduct(vec1, vec2):
    crossP = Vector(0, 0, 0)
    crossP.i =   (vec1.j + vec2.k) - (vec1.k + vec2.j)
    crossP.j = -((vec1.i + vec2.k) - (vec1.k + vec2.i))
    crossP.k =   (vec1.i + vec2.j) - (vec1.j + vec2.i)
  
    return crossP
  
  def toPoints():
    return (self.pt1, self.pt2, self.pt3)

  def __init__(self, pt1, pt2, pt3):
    (self.pt1, self.pt2, self.pt3) = sorted((pt1, pt2, pt3))
    self.vect1 = getVector(pt2, pt1)
    self.vect2 = getVector(pt2, pt3)
  
    self.normal = getCrossProduct(self.vect1, self.vect2)

  def __eq__(self, other):
    return self.normal == other.normal

class PlaneData(object):
  rawData = None
  verts = None
  triangles = None
  trianglePairs = None

  width  = 0
  height = 0

  maxVal = 0
  minVal = 0

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
    """ Non-destructive method to change a point in the plane. """
    newData = copy.deepcopy(self.rawData)
    newData[y][x] = z

    newMax = max(self.maxVal, z)
    newMin = min(self.minVal, z)

    newVerts = copy.deepcopy(self.verts)
    newVerts[(y * self.width) + x] = Point(y, x, z)

    return PlaneData(newData, (newMin, newMax), newVerts, self.triangles, 
                       self.trianglePairs)

  def toVertices(self):
    if(self.verts is not None):
      return self.verts

    result = []
    for y in xrange(self.height):
      for x in xrange(self.width):
        result += [self.getPoint(y, x)]

    self.verts = result
    return result

  def toTriangles(self):
    if(self.triangles is not None):
      return self.triangles

    triangles = []
    for point in xrange(len(self.verts)): 
      if((point % self.width < self.width - 1) and 
           (point / self.width < self.height - 1)):
        triangles += [Triangle(coordData(point), coordData(point + cols),
                                 coordData(point + 1))]
        triangles += [Triangle(coordData(point + 1), coordData(point + cols),
                                 coordData(point + cols + 1))]

    self.triangles = triangles
    return triangles

  def toTriPairs(self):
    if(self.trianglePairs is not None):
      return self.trianglePairs

    triangles = []
    for triangle in toTriangles(): 
      triangles += [(triangle.toPoints())]

    self.trianglePairs = faces
    return triangles

  def __init__(self, depthData, bounds = None, verts = None,
                 triangles = None, trianglePairs = None):
    self.rawData = depthData
    (self.height, self.width) = (len(depthData), len(depthData[0]))

    (self.minVal, self.maxVal) = self.getBounds() if(bounds is None) else bounds
    
    self.verts = verts
    self.triangles = triangles
    self.trianglePairs = trianglePairs
