import threading
import Queue
import time

import freenect
from freenect import sync_get_depth as getDepth
from src.tools import errors, plane, optimize, filters, writer

class Worker(threading.Thread):
  errorVal = 2047.0

  # In degrees
  triangleNormalRadix = 5

  def __init__(self, mapDir = "", queueMax = 3):
    self.queueMax = queueMax
    self.physicsQueue = Queue.Queue(queueMax)
    self.graphicsQueue = Queue.Queue(queueMax)

    self.mapDir = mapDir

    self.exit = False
    self.kinectDetected = False
    threading.Thread.__init__(self)

  def setPlaneName(name):
    self.planeName = name
    self.path = (self.mapDir +"/"+ name if(self.mapDir != "") else name)+".csv"
    try:
      open(self.path).close()
      self.fileExists = True
    except:
      self.fileExists = False

    return self.fileExists

  def run(self):
    while(not(self.exit)):
      startTime = time.time()
      data = getDepth()

      if(data is None):
        self.stop()
        continue

      self.kinectDetected = True

      (self.rawData, _) = data
      self.rawData = self.rawData.tolist()

      self.dataPlane = plane.PlaneData(self.rawData, self.planeName)

      self.dataPlane = errors.averageErrors(self.dataPlane, Worker.errorVal)
      self.dataPlane = filters.flipSurface(self.dataPlane)

      writer.writePlaneToFile(self.dataPlane, self.path)
      #self.dataPlane = optimize.groupTriangles(self.dataPlane)

      if(not(self.physicsQueue.full())): self.physicsQueue.put(self.dataPlane) 
      if(not(self.graphicsQueue.full())):
         self.graphicsQueue.put(self.dataPlane)
      
      # Only one loop for testing purposes
      self.stop()

  def stop(self):
    # Properly stop using the Kinect
    freenect.sync_stop()

    self.exit = True
