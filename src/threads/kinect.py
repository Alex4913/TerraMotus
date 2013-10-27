import threading
import Queue
import time

from freenect import sync_get_depth as getDepth
from src.tools import errors, plane, optimize

class Worker(threading.Thread):
  errorVal = 2047.0

  exit = False

  # In degrees
  triangleNormalRadix = 5

  hasData = False
  kinectDetected = False

  queueMax = None
  physicsQueue = Queue.Queue()
  graphicsQueue = Queue.Queue()

  def __init__(self, queueMax = 0):
    self.queueMax = queueMax
    physicsQueue = Queue.Queue(queueMax)
    graphicsQueue = Queue.Queue(queueMax)
    threading.Thread.__init__(self)

  def run(self):
    while(not(self.exit)):
      try:
        with nout.noSTDOut():
          self.rawData = getDepth()
        self.kinectDetected = True
      except:
        self.kinectDetected = False
        continue

      self.dataPlane = PlaneData(self.rawData)
      self.dataPlane = errors.averageErrors(self.dataPlane, errorVal)
      self.dataPlane = optimize.groupTriangles(self.dataPlane)

  def stop(self):
    self.exit = True
