def tryAssign(data, row, col, defaultVal):
  try:
    return data[row][col]
  except:
    return defaultVal

def getNeighbors(data, row, col):
  defaultVal = None

  # Return (North, East, South, West)
  return (tryAssign(data, row - 1, col, defaultVal),
          tryAssign(data, row, col + 1, defaultVal),
          tryAssign(data, row + 1, col, defaultVal),
          tryAssign(data, row, col - 1, defaultVal))

def isSimilarToNeighbors(data, row, col, radix):
  neigbors = getNeighbors(data, row, col)

  for neighbor in neighbors:
    if(neigbor is not None):
      if(abs(neighbor - data[row][col]) > radix):
        return False

  return True
