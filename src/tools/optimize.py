from src.tools import plane, neighborhood

class TriangleGroup(object):
  rawPoints = None
  width = None
  height = None

  minX = None
  maxX = None
  minY = None
  maxY = None

  def getWidth(self, rawPoints):
    maxX = None
    minX = None
    for triangle in rawPoints:
      for point in triangle.toPoints():
        maxX = max(maxX, point.x) if(maxX is not None) else point.x
        minX = min(minX, point.x) if(minX is not None) else point.x

    return (minX, maxX, maxX - minX)
  
  def getHeight(self, rawPoints):
    maxY = None
    minY = None
    for triangle in rawPoints:
      for point in triangle.toPoints():
        maxY = max(maxY, point.y) if(maxY is not None) else point.y
        minY = min(minY, point.y) if(minY is not None) else point.y

    return (minY, maxY, (maxY - minY))

  def getPointTracker(self, rawPoints):
    tracker = [ [None] * self.width for row in xrange(self.width)]
    for triangle in self.rawPoints:
      for point in triangle.toPoints():
        tracker[point.y - self.minY][point.x - minX] = False

    return tracker

  def __init__(self, rawPoints):
    self.rawPoints = rawPoints
    (self.minX, self.maxX, self.width) = getWidth()
    (self.minY, self.maxY, self.height) = getHeight()    

    self.triangles = rawToTriangles(rawPoints)
    self.tracker = getPointTracker(rawPoints)


def obstaclesInPath(trigroup, x, y, (dx, dy)):
  pass

def largestBoxFromLocation(trigroup, x, y, (dx, dy)):
  pass

def chooseDirection(trigroup, edges, x, y):
  pass

def findLargestBox(triGroup, edges):
  usedEdges = []
  for edge in edges:
    if(edge not in usedEdges):
      pass

def removeBorderTriangles(triGroup, edges): 
  for point in xrange(1, len(edges)):
    pass

def getEdgesGroup(triGroup):
  edges = []
  data = triGroup.getPointTracker()

  # Cheat a bit and take advantage of this nice object
  cheatPlane = plane.PlaneData(data, (0, 0))

  for point in cheatPlane.toVertices():
    neighborhood.getNeighbors(cheatPlane)

    for neighbor in neighbors:
      if(neighbor is None):
        edges += [point]
        break

  return edges

def groupTriangles(dataPlane, radix):
  pass

def optimize(dataPlane, radix):
  pass
