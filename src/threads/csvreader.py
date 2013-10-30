import threading
import Queue
import time

from src.tools import errors, optimize, parser, plane

class Worker(threading.Thread):
  fileName = "data.csv"
  errorVal = 2047.0

  # In degrees
  triangleNormalRadix = 5

  def __init__(self, queueMax = 3):
    self.queueMax = queueMax
    self.physicsQueue = Queue.Queue(queueMax)
    self.graphicsQueue = Queue.Queue(queueMax)

    try:
      open(Worker.fileName).close()
      self.fileExists = True
    except:
      self.fileExists = False

    self.exit = False
    threading.Thread.__init__(self)

  def run(self):
    while(not(self.exit)):
      try:
        self.rawData = parser.parse(Worker.fileName)
        self.fileRead = True
        
        self.dataPlane = plane.PlaneData(self.rawData)
        self.dataPlane = errors.averageErrors(self.dataPlane, Worker.errorVal)
        #self.dataPlane = optimize.groupTriangles(self.dataPlane)

        if(not(self.physicsQueue.full())): self.physicsQueue.put(self.dataPlane)
        if(not(self.graphicsQueue.full())): 
          self.graphicsQueue.put(self.dataPlane)

      except:
        self.fileRead = False
        continue

  def stop(self):
    self.exit = True
