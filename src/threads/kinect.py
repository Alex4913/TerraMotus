import threading
import Queue
import time

from freenect import sync_get_depth as getDepth
from src.tools import errors, plane, optimize

class Worker(threading.Thread):
  errorVal = 2047.0

  # In degrees
  triangleNormalRadix = 5

  def __init__(self, queueMax = 0):
    self.queueMax = queueMax
    self.physicsQueue = Queue.Queue(queueMax)
    self.graphicsQueue = Queue.Queue(queueMax)

    self.exit = False
    self.kinectDetected = False
    threading.Thread.__init__(self)

  def run(self):
    while(not(self.exit)):
      try:
        with nout.noSTDOut():
          self.rawData = getDepth()

        self.kinectDetected = True

        self.dataPlane = PlaneData(self.rawData)
        self.dataPlane = errors.averageErrors(self.dataPlane, Worker.errorVal)
        #self.dataPlane = optimize.groupTriangles(self.dataPlane)

      except:
        self.kinectDetected = False
        continue

  def stop(self):
    self.exit = True
