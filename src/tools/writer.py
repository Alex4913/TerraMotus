def writePlaneToFile(dataPlane, path):
  f = open(path, "w")
  for row in xrange(dataPlane.height):
    temp = str(dataPlane.rawData[row][0])
    for col in xrange(1, dataPlane.width):
      temp += "," + str(dataPlane.rawData[row][col])

    f.write(temp + "\n")
  f.close()
