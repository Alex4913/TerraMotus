from src.tools import plane as plane

def getNeighbor(row, col, (dy, dx), array, height, width):
  row += dy
  col += dx

  if((col < 0 or col >= width) or (row < 0 or row >= height)):
    return None
  else:
    return array[row][col]

def getListNeighbors(row, col, array):
  (rows, cols) = (len(array), len(array[0]))
  ptUp    = getNeighbor(row, col, ( 0, -1), array, rows, cols)
  ptDown  = getNeighbor(row, col, ( 0,  1), array, rows, cols)
  ptLeft  = getNeighbor(row, col, (-1,  0), array, rows, cols)
  ptRight = getNeighbor(row, col, ( 1,  0), array, rows, cols)
  
  return (ptUp, ptRight, ptDown, ptLeft)

def getPlaneNeighbors(point, dataPlane): 
  ptUp    = getNeighbor(point.y, point.x, ( -1, 0), dataPlane.rawData,
                          dataPlane.height, dataPlane.width)
  ptDown  = getNeighbor(point.y, point.x, ( 1,  0), dataPlane.rawData,
                          dataPlane.height, dataPlane.width)
  ptLeft  = getNeighbor(point.y, point.x, ( 0, -1), dataPlane.rawData,
                          dataPlane.height, dataPlane.width)
  ptRight = getNeighbor(point.y, point.x, ( 0,  1), dataPlane.rawData,
                          dataPlane.height, dataPlane.width)

  if(ptUp is not None): ptUp = plane.Point(point.x, point.y-1, ptUp)
  if(ptDown is not None): ptDown = plane.Point(point.x, point.y-1, ptDown)
  if(ptLeft is not None): ptLeft = plane.Point(point.x, point.y-1, ptLeft)
  if(ptRight is not None): ptRight = plane.Point(point.x, point.y-1, ptRight)

  return (ptUp, ptRight, ptDown, ptLeft)
