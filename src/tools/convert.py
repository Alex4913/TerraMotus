def depthToVertices(data):
  vertices = []
  for row in xrange(len(data)):
    for col in xrange(len(data[row])):
      vertices += [(row, col, float(data[row][col]))]

  return vertices

def depthToODEFaces(data, verts = None):
  if(verts is None):
    verts = depthToVertices(data)

  maxX = len(data[0])
  maxY = len(data)

  faces = []
  for point in xrange(len(verts)):
    if((point % maxX < maxX - 1) and (point / maxX < maxY - 1)):
      pt1 = (point, point + 1, point + maxX)
      pt2 = (point + 1, point + maxX, point + maxX + 1)
      faces += [pt1]
      faces += [pt2]

  return faces
