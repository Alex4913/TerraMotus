def depthToVertices(data):
  vertices = []
  for row in xrange(len(data)):
    for col in xrange(len(data[row])):
      vertices += [(row, col, float(data[row][col]))]

  return vertices

def depthToODEFaces(data, verts = None):
  if(verts is None):
    verts = depthToVertices(data)

  rows = len(data)
  cols = len(data[0])

  faces = []
  for point in xrange(len(verts)):
    if((point % cols < cols - 1) and (point / cols < rows - 1)):
      pt1 = (point, point + 1, point + cols)
      pt2 = (point + 1, point + cols, point + cols + 1)
      faces += [pt1]
      faces += [pt2]

  return faces

def depthToGLFaces(data, verts = None):
  if(verts is None):
    verts = depthToVerticies(data)

  rows = len(data)
  cols = len(data[0])

  faces = []
  for point in xrange(len(verts)): 
    if((point % cols < cols - 1) and (point / cols < rows - 1)):
      faces += [(point, point + cols, point + 1, point + cols + 1)]

  return faces

def depthToMergedGLFaces(data, verts = None):
  if(verts is None): verts = depthToVerticies(data)

  (rows, cols) = (len(data), len(data[0]))
  
  (faces, point) = ([], 0)
  while(point < len(verts)):
    if((point % cols < cols - 1) and (point / cols < rows - 1)):
      # For the first triangle in the strip
      if(point % cols == 0):
        faces += [(point, point + cols, point + 1, point + cols + 2)]
        point += 1

      # If the point is two columns away from the end of the row and needs
      # special attention
      elif(point % cols == cols - 1 - 2):
        faces += [(point, point + cols + 1, point + 2, point + cols + 2)]
        point += 2
        if(cols % 2 == 1):
          faces += [(point, point + cols, point + 1, point + cols + 1)]
          point += 1
      
      # For triangles between the end and the beginning
      else:
        faces += [(point, point + cols + 1, point + 2, point + cols + 3)]
        point += 2

    else:
      point += 1

  return faces
