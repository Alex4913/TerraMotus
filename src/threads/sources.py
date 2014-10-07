import threading
from multiprocessing import Queue

import os
import time

import freenect
from src.tools import plane, parser, writer

class DataSource(threading.Thread):
  """
  A class to represent a stream of data that supplies a 2D array of data.

  The class has a few standard methods which are intended to be over-written,
  all of which are methods from the super class, Thread. It is intended to be
  run in parallel to simulation, and it has a Queue to safely access the data
  that is created from the class.

  This class is intended to be fed to the Converter class.
  """

  def __init__(self, queueMax = 1):
    """
    Init the DataSource as a Thread with a Queue.

    Keyword Arguments:
    queueMax -- The maximum number of data points to be held within the Queue
      (default 1)
    """

    self.queueMax = queueMax
    self.queue = Queue(queueMax)

    self.error = False
    threading.Thread.__init__(self)

  def add(self, data):
    """
    Add a point of data to the Queue.

    Make sure the Queue is not full before adding the new data.

    Keyword Arguments:
    data -- The data to be added to the Queue
    """

    if(not(self.queue.full())): self.queue.put(data)

  def get(self):
    """
    Get a point of data from the Queue.

    Make sure the Queue is not empty before removing a data point from the
    Queue.

    Returns:
      The least recent data-point in the Queue. (first in, first out)
    """

    if(not(self.queue.empty())): return self.queue.get()

class CSVSource(DataSource):
  """
  A class to represent a CSV stream of data.

  Continually reads in a CSV file, and appends the contents to the inherited
  Queue. Thus, any changes made to the data in the file will update the
  data pushed to the Queue.
  """

  def __init__(self, name, mapDir = "", queueMax = 1):
    """
    Init the CSVSource, given a path to the CSV file, and the name of the
    file to read in.

    Keyword Arguments:
    name -- The name of the file to be read in
    mapDir -- The directory containing the file (default "")
    queueMax -- The maximum number of data points to be held in the Queue
      (default 1)
    """

    super(CSVSource, self).__init__(queueMax)
    self.mapDir = mapDir
    self.name = name
    self.exit = False

    # Generate a path and the name of the plane given the base name of the file
    self.setPlaneName(self.name)

  def setPlaneName(self, name):
    """
    Generate necessary constants based on a supplied name

    Keyword Arguments:
    name -- the name of the CSV file
    """

    self.planeName = name
    self.path = self.mapDir +"/"+ name if(self.mapDir != "") else name

    # If the file does not exist or is a directory, set the error value to True
    self.error=not(os.path.exists(self.path) and not(os.path.isdir(self.path)))

  def run(self):
    """
    Override the super-super class's run method (Thread.run()) for the CSVSource
    Thread.
    """

    # Stop if there was an error detected
    if(self.error): self.stop()

    # Keep going unless stopped
    while(not(self.exit)):
      try:
        # Attempt to add data to the Queue
        data = plane.PlaneData(parser.parse(self.path), self.name)
        self.add(data)
      except:
        continue

  def stop(self):
    """
    Set a variable to stop Thread execution by terminating the while loop in
    run().
    """
    self.exit = True

class KinectSource(DataSource):
  """
  A class to represent a stream of data from the Microsoft Kinect.

  Continually reads data from the Kinect, and appends the contents to the 
  inherited Queue. Thus, any changes made to the data in the Kinect's Field of 
  View will update the data pushed to the Queue.
  """

  # A name with a Unix timestamp for writing the data to a file
  name = "kinect-data-%d.csv" % (int(time.time()))

  def __init__(self, queueMax = 1):
    """
    Init the KinectSource.

    Also, check to see if a Kinect is present or is available for use.

    Keyword Arguments:
    queueMax -- The maximum number of data points to be held in the Queue
      (default 1)
    """

    super(KinectSource, self).__init__(queueMax)
    self.exit = False

    # Set the error value based on if data can be read from the Kinect
    try: self.error = (freenect.sync_get_depth() is None)
    except: self.error = True

  def detect(self):
    """
    Look for a Kinect attached to the computer.

    Returns:
      If a Kinect was found and is available for use
    """

    detected = False
    try: detected = (freenect.sync_get_depth() is not None)
    except: pass

    self.error = not detected
    return detected

  def run(self):
    """
    Override the super-super class's run method (Thread.run()) for the 
    KinectSource Thread.
    """

    # Stop if there was an error
    if(self.error): self.stop()

    while(not(self.exit)):
      try:
        # Stop the thread if there is no data returned
        data = freenect.sync_get_depth()
        if(data is None):
          self.stop()

        # Unpack the data, ignoring one of the values
        (data, _) = data

        # Create a data point
        data = plane.PlaneData(data.tolist(), KinectSource.name)
        self.add(data)
      except: continue

  def stop(self):
    """
    Safely stop the Kinect Thread, freeing the Kinect properly.

    Set a variable to stop Thread execution by terminating the while loop in
    run().
    """

    freenect.sync_stop()
    self.exit = True
