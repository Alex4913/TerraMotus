import threading
import Queue
import time

from src.tools import errors, optimize2 as optimize, parser, plane, filters

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
    threading.Thread.__init__(self)

  def setPlaneName(self, name):
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
      try:
        self.rawData = parser.parse(self.path)
        
        self.dataPlane = plane.PlaneData(self.rawData, self.planeName)
        self.dataPlane = errors.averageErrors(self.dataPlane, Worker.errorVal)
        self.dataPlane = filters.averagePass(self.dataPlane, 2)

#        betterData = optimize.Optimize(self.dataPlane, self.triangleNormalRadix)
#        self.dataPlane = betterData

        if(not(self.physicsQueue.full())): self.physicsQueue.put(self.dataPlane)
        if(not(self.graphicsQueue.full())): 
          self.graphicsQueue.put(self.dataPlane)

        self.stop()

      except:
        pass

  def stop(self):
    self.exit = True
