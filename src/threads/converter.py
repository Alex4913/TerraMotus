import multiprocessing
from multiprocessing import Queue

import time
import os

from src.threads import sources
from src.tools import errors, plane, optimize, filters, writer

class Converter(multiprocessing.Process):
  """
  A class to convert a stream of data to the required data structures for
  ODE and OpenGL.

  This takes a instance of a DataSource and converts the data it supplies
  in its Queue to a usable type for ODE and OpenGL. This also saves data
  from the Kinect DataSource as a CSV file after the transformations.


  This also applies some transformations on the data, given its type:
    Kinect Data: Removes errors, flips the surface and averages the data
    CSV Data: Pipes the data directly to the conversion methods without
    transformation.
  """

  # The value that the Kinect returns to represent errors
  errorVal = 2047.0

  def __init__(self, dataSource, mapDir = "", queueMax = 1):
    """
    Initialize the Converter class.

    Create two Queues for Thread / Multiprocessor safe comminucation of 
    the converted Data, one for the Physics Thread, one for the Display Thread.

    Keyword Arguments:
    dataSource -- An instance of a DataSource to be used for conversion
    mapDir -- The directory that the maps are stored in (default "")
    queueMax -- The maximum number of stored versions of converted data
    """

    # Queue Items
    self.queueMax = queueMax
    self.physicsQueue = Queue(queueMax)
    self.graphicsQueue = Queue(queueMax)

    # Constants from the constructor
    self.dataThread = dataSource
    self.mapDir = mapDir
    
    # Variables to store various states of the thread
    self.error = False
    self.exit = False
    self.ready = False
    
    # Start the thread and the other process
    multiprocessing.Process.__init__(self)
    self.dataThread.start()

  def stripExtension(self, path):
    """
    Remove the file extension given its path, if it exists.

    Keyword Arguments:
    path -- path to the file
    """
    
    # Get the filename
    filename = path.split("/")[-1]

    # Remove the part after the last dot
    noExtension = filename.split(".")[:-1]

    # Restore any periods within the filename
    return ".".join(noExtension)
 
  def getOutPath(self, name):
    """
    Generate an overwrite-safe file path for a given name.

    Add numbers to the end of the filename to avoid over-writing
    an existing filename.

    Keyword Arguments:
    name -- The desired name of the file

    Returns:
      A safe path to an available file
    """

    # Add a number to the end of the file if one exists already
    # to avoid over-writing
    newName = name
    count = 1
    while(os.path.exists(newName)):
      newName = self.stripExtension(name) + str(count) + ".csv"

    # Return a path to the file, taking into account the mapDir
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
        dataPlane = errors.averageErrors(dataPlane, Converter.errorVal)
        dataPlane = filters.flipSurface(dataPlane)
        self.export(dataPlane)
      dataPlane = filters.averagePass(dataPlane, 5)

      if(not(self.physicsQueue.full())): self.physicsQueue.put(dataPlane)
      if(not(self.graphicsQueue.full())): self.graphicsQueue.put(dataPlane)
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
