import threading
import Queue
import time
import os

from src.threads import sources
from src.tools import errors, plane, optimize, filters, writer

class Converter(threading.Thread):
  errorVal = 2047.0

  def __init__(self, dataSource, queueMax = 3):
    self.queueMax = queueMax
    self.physicsQueue = Queue.Queue(queueMax)
    self.graphicsQueue = Queue.Queue(queueMax)

    self.dataThread = dataSource
    self.error = False
    self.exit = False
    self.ready = False
    threading.Thread.__init__(self)
    self.dataThread.start()

  def stripExtension(self, path):
    # Get rid of .xxx
    return path[:len(path) - 4]
 
  def getOutPath(self, name):
    # Add a number to the end of the file if one exists already
    # to avoid over-writing
    newName = name
    count = 1
    while(os.path.exists(newName)):
      newName = self.stripExtension(name) + str(count) + ".csv"

    return self.mapDir +"/"+ newName if(self.mapDir != "") else newName

  def run(self):
    self.error = self.dataThread.error
    if(self.dataThread.error):
      self.stop()

    while(not(self.exit)):
      dataPlane = self.dataThread.get()

      if(dataPlane is None):
        continue

      dataPlane = errors.averageErrors(dataPlane, Converter.errorVal)
      dataPlane = filters.flipSurface(dataPlane)
      dataPlane = filters.averagePass(dataPlane, 2)

      if(not(self.physicsQueue.full())): self.physicsQueue.put(dataPlane)
      if(not(self.graphicsQueue.full())): self.graphicsQueue.put(dataPlane)
      self.dataPlane = dataPlane
      self.ready = True

  def stop(self):
    self.dataThread.stop()
    self.exit = True

  def export(self):
    path = self.getOutPath(self.dataPlane.name)
    writer.writePlaneToFile(self.dataPlane, path)
