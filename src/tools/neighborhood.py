from src.tools import plane

def getNeighbor(point, (dx, dy), dataPlane):
  point.x = point.x + dx
  point.y = point.y + dy

  if((point.x < 0 or point.x >= dataPlane.width) or
       (point.y < 0 or point.y >= dataPlane.height))
    return None
  else:
    return dataPlane.getPoint(point.y, point.x)

def getNeighbors(point, dataPlane):
  ptUp    = getNeighbor(point, ( 0, -1), dataPlane)
  ptDown  = getNeighbor(point, ( 0,  1), dataPlane)
  ptLeft  = getNeighbor(point, (-1,  0), dataPlane)
  ptRight = getNeighbor(point, ( 1,  0), dataPlane)

  return (ptUp, ptRight, ptDown, ptLeft)

def isSimilarToNeighbors(point, dataPlane):
  neigbors = getNeighbors(point, dataPlane)

  for neighbor in neighbors:
    if((neigbor is not None) and (abs(neighbor.z - point.z) > radix)):
      return False

  return True
