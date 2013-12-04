import multiprocessing
#import threading
from multiprocessing import Queue
import time
import os

from src.threads import sources
from src.tools import errors, plane, optimize, filters, writer

class Converter(multiprocessing.Process):
  errorVal = 2047.0

  def __init__(self, dataSource, mapDir = "", queueMax = 1):
    self.queueMax = queueMax
    self.physicsQueue = Queue(queueMax)
    self.graphicsQueue = Queue(queueMax)

    self.dataThread = dataSource
    self.mapDir = mapDir
    self.error = False
    self.exit = False
    self.ready = False
    multiprocessing.Process.__init__(self)
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

      if(isinstance(self.dataThread, sources.KinectSource)):
        print "Errors"
        dataPlane = errors.averageErrors(dataPlane, Converter.errorVal)
        print "Flip"
        dataPlane = filters.flipSurface(dataPlane)
      print "Average"
      dataPlane = filters.averagePass(dataPlane, 2)
      print "Done"

      if(not(self.physicsQueue.full())): self.physicsQueue.put(dataPlane)
      if(not(self.graphicsQueue.full())): self.graphicsQueue.put(dataPlane)
      self.export(dataPlane)
      self.stop()

  def getReady(self):
    return self.ready

  def terminate(self):
    self.stop()
    multiprocessing.Process.terminate(self)

  def stop(self):
    self.dataThread.stop()
    self.exit = True

  def export(self, dataPlane):
    path = self.getOutPath(dataPlane.name)
    writer.writePlaneToFile(dataPlane, path)
