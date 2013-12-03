import copy
from src.tools import plane, neighborhood

def flipSurface(dataPlane):
  rawData = copy.deepcopy(dataPlane.rawData)

  for row in xrange(dataPlane.height):
    for col in xrange(dataPlane.width):
      rawData[row][col] = -rawData[row][col] + dataPlane.maxVal

  return plane.PlaneData(rawData, dataPlane.name)

def sample(dataPlane, sampleStep):
  rawData = dataPlane.rawData
  newData = []
  for row in xrange(0, dataPlane.height, sampleStep):
    temp = []
    for col in xrange(0, dataPlane.width, sampleStep):
      temp += [rawData[row][col]]

    newData += [temp]

  return plane.PlaneData(newData, dataPlane.name)

def averagePass(dataPlane, passNum = 1):
  backupData = copy.deepcopy(dataPlane.rawData)

  for loop in xrange(passNum):
    reference = copy.deepcopy(backupData)

    for row in xrange(dataPlane.height):
      for col in xrange(dataPlane.width):

        neighbors = neighborhood.getListNeighbors(row, col, reference)
        sumOfNeighbors = 0
        validNeighbors = 0

        for neighbor in neighbors:
          if(neighbor is not None):
            sumOfNeighbors += neighbor
            validNeighbors += 1

        backupData[row][col] = (float(sumOfNeighbors) / validNeighbors)

  return plane.PlaneData(backupData, dataPlane.name)
