import neighborhood
import copy

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

def averageErrors(dataPlane, errorVal):
  hasErrors = containsErrors(dataPlane, errorVal)
  if(not(hasErrors)):
    return data
 
  dataPlaneCopy = copy.deepcopy(dataPlane)
  while(hasErrors):
    points = getFringeErrorPoints(dataPlaneCopy, errorVal)

    for point in points:
      neighbors = neighborhood.getNeighbors(point, dataPlaneCopy)

      validNeighbors = 0
      sumOfNeighbors = 0

      for neighbor in neighbors:
        if((neighbor is not None) and (neighbor.z != errorVal)):
          sumOfNeighbors += neighbor.z
          validNeighbors += 1

      point.z = sumOfNeighbors / validNeighbors
      dataPlaneCopy = dataPlaneCopy.setPoint(point.x, point.y, point.z)

    hasErrors = containsErrors(dataPlaneCopy, errorVal)

  return dataPlaneCopy
