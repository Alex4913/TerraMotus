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

def sampleData(data, sampleStep):
  rows = len(data)
  cols = len(data[0])

  returnData = []
  for row in xrange(0, rows, sampleStep):
    temp = []
    for col in xrange(0, cols, sampleStep):
      temp += data[row][col]
    returnData += temp

  return returnData

def averageData(data, stepSize):
  rows = len(data)
  cols = len(data[0])

  returnData = []
  for row in xrange(stepSize, rows, stepSize):
    temp = []
    for col in xrange(stepSize, cols, stepSize):
      sumOfArea = 0
      for subRow in xrange(row, row - stepSize, -1):
        for subCol in xrange(col, col - stepSize, -1):
          sumOfArea += data[subRow][subCol]

      temp += [float(sumOfArea) / (stepSize ** 2)]

    returnData += temp

  return returnData

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
