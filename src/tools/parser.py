import copy

def stringArrayToFloat(array):
  """ Convert a 2D list with string values to the same list with floats """
  returnArray = []
  for row in array:
    rowData = []
    for col in row:
      rowData += [float(col)]
    returnArray += [rowData]

  return returnArray

def parse(planeName):
  """ Open a data CSV and return a 2D list of floats """
  f = open(planeName, 'r')
  data = []
  for line in f:
    data += [line.split(',')] 

  f.close()
  return stringArrayToFloat(data)
