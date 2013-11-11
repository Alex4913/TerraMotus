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
    neighbors = neighborhood.getPlaneNeighbors(point, dataPlane)

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

def averageFringeValues(dataPlane, errorVal):
  points = getFringeErrorPoints(dataPlane, errorVal)

  while(len(points) > 0):
    for point in points:
      neighbors = neighborhood.getPlaneNeighbors(point, dataPlane)

      validNeighbors = 0
      sumOfNeighbors = 0

      for neighbor in neighbors:
        if((neighbor is not None) and (neighbor.z != errorVal)):
          sumOfNeighbors += neighbor.z
          validNeighbors += 1

      dataPlane.setPoint(point.x, point.y, float(sumOfNeighbors)/validNeighbors)

    points = getFringeErrorPoints(dataPlane, errorVal)

  return dataPlane

def averageErrors(dataPlane, errorVal):
  return averageFringeValues(dataPlane, errorVal)
