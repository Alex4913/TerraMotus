import csv
import copy

def stringArrayToFloat(array):
  """ Convert a 2D list with string values to the same list with floats """
  returnArray = []
  for row in array:
    rowData = []
    for col in row:
      if(rowData == []):
        rowData = [float(col)]
      else:
        rowData += [float(col)]

    if(returnArray == []):
      returnArray = [rowData]
    else:
      returnArray += [rowData]

  return returnArray

def parse(fileName):
  """ Open a data CSV and return a 2D list of floats """
  f = open(fileName, 'r')
  reader = csv.reader(f, delimiter=',')

  data = []
  for row in reader:
    if(data == []):
      data = [row]
    else:
      data += [row]
  
  data = stringArrayToFloat(data)
  
  return data
