import neighborhood
import copy

def getMax(data, startVal = 0):
  result = startVal
  for row in data:
    result = max(max(row), result)

  return result

def getMin(data, startVal):
  result = startVal
  for row in data:
    result = min(min(row), result)

  return result

def getErrorLocations(data, errorVal):
  (rows, cols) = (len(data), len(data[0]))

  points = []
  for row in xrange(rows):
    for col in xrange(cols):
      if(data[row][col] == errorVal):
        points += [(row, col)]

  return points

def getFringeErrorLocations(data, errorVal):
  (rows, cols) = (len(data), len(data[0]))
  
  points = []
  for row in xrange(rows):
    for col in xrange(cols):
      neighbors = neighborhood.getNeighbors(data, row, col)
      if(data[row][col] == errorVal):
        for neighbor in neighbors:
          if((neighbor is not None) and (neighbor != errorVal)):
            points += [(row, col)]
            break

  return points

def containsErrors(data, errorVal):
  (rows, cols) = (len(data), len(data[0]))
  
  for row in xrange(rows):
    for col in xrange(cols):
      if(data[row][col] == errorVal):
        return True

  return False

def averageErrors(data, errorVal):
  hasErrors = containsErrors(data, errorVal)
  if(not(hasErrors)):
    return data
 
  dataCopy = copy.deepcopy(data)
  while(hasErrors):
    errorValLocations = getFringeErrorLocations(dataCopy, errorVal)

    for errorValLocation in errorValLocations:
      (row, col) = errorValLocation
      neighbors = neighborhood.getNeighbors(dataCopy, row, col)

      validNeighbors = 0
      sumOfNeighbors = 0

      for neighbor in neighbors:
        if((neighbor is not None) and (neighbor != errorVal)):
          sumOfNeighbors += neighbor
          validNeighbors += 1

      dataCopy[row][col] = sumOfNeighbors / validNeighbors

    hasErrors = containsErrors(dataCopy, errorVal)

  return dataCopy
