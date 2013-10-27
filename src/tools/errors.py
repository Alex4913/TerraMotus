import neighborhood
import copy, time

from src.tools import plane
###############################################################################
#                              Error Correction                               #
###############################################################################
def getErrorPoints(dataPlane, errorVal):
  points = []
  for point in dataPlane.toVertices():
    if(point.z == errorVal):
      points += [point]

  return points

def getFringeErrorPoints(dataPlane, errorVal):
  points = []
  for point in dataPlane.toVertices():
    neighbors = neighborhood.getNeighbors(point, dataPlane)

    if(point.z == errorVal): 
     for neighbor in neighbors:
       if((neighbor is not None) and (neighbor.z != errorVal)):
         points += [point]
         break

  return points

def containsErrors(dataPlane, errorVal):
  for point in dataPlane.toVertices():
    if(point.z == errorVal):
      return True

  return False

def averageRegularValues(dataPlane, errorVal):
  points = getErrorPoints(dataPlane, errorVal)

  for point in points:
    neighbors = neighborhood.getNeighbors(point, dataPlane)

    validNeighbors = 0
    sumOfNeighbors = 0

    for neighbor in neighbors:
      if((neighbor is not None) and (neighbor.z != errorVal)):
        sumOfNeighbors += neighbor.z
        validNeighbors += 1

    point.z = sumOfNeighbors / validNeighbors
    startTime2 = time.time()
    dataPlane.setPoint(point.x, point.y, point.z)

  print len(getErrorPoints(dataPlane, errorVal))
  return dataPlane

def averageFringeValues(dataPlane, errorVal):
  points = getFringeErrorPoints(dataPlane, errorVal)

  errorsLeft = len(points)
  while(errorsLeft > 0):
    for point in points:
      neighbors = neighborhood.getNeighbors(point, dataPlane)

      validNeighbors = 0
      sumOfNeighbors = 0

      for neighbor in neighbors:
        if((neighbor is not None) and (neighbor.z != errorVal)):
          sumOfNeighbors += neighbor.z
          validNeighbors += 1

      point.z = sumOfNeighbors / validNeighbors
      dataPlane.setPoint(point.x, point.y, point.z)

    points = getFringeErrorPoints(dataPlane, errorVal)
    errorsLeft = len(points)

  return dataPlane

def averageErrors(dataPlane, errorVal):
  dataPlane = averageFringeValues(dataPlane, errorVal)
  #dataPlane = averageRegularValues(dataPlane, errorVal)
  return dataPlane
