from src.tools import plane

class TriangleGroup(object):
  rawPoints = None
  width = None
  height = None

  def getWidth(self, rawPoints):
    maxX = None
    minX = None
    for triangle in rawPoints:
      for point in triangle.toPoints():
        maxX = max(maxX, point.x) if(maxX is not None) else point.x
        minX = min(minX, point.x) if(minX is not None) else point.x

    # Convert to 1-based not 0-based
    return (maxX - minX) + 1
  
  def getHeight(self, rawPoints):
    maxY = None
    minY = None
    for triangle in rawPoints:
      for point in triangle.toPoints():
        maxY = max(maxY, point.y) if(maxY is not None) else point.y
        minY = min(minY, point.y) if(minY is not None) else point.y

    # Convert to 1-based not 0-based
    return (maxY - minY) + 1

  def __init__(self, rawPoints):
    self.rawPoints = rawPoints
    self.width = getWidth()
    self.height = getHeight()    

    

  def add(triangle):
    triangles += [triangle]

def findLargestTriangle(triGroup):
  pass

def groupTriangles(dataPlane, radix):
  pass

def optimize(dataPlane, radix):
  pass
