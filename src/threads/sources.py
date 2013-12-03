import threading
import Queue
import os

import freenect
from src.tools import plane, parser, writer

class DataSource(threading.Thread):
  def __init__(self, queueMax = 3):
    self.queueMax = queueMax
    self.queue = Queue.Queue(queueMax)

    self.error = False
    threading.Thread.__init__(self)

  def add(self, data):
    if(not(self.queue.full())): self.queue.put(data)

  def get(self):
    if(not(self.queue.empty())): return self.queue.get()

class CSVSource(DataSource):
  def __init__(self, name, mapDir = "", queueMax = 3):
    super(CSVSource, self).__init__(queueMax)
    self.mapDir = mapDir
    self.name = name
    self.exit = False

    self.setPlaneName(self.name)

  def setPlaneName(self, name):
    self.planeName = name
    self.path = self.mapDir +"/"+ name if(self.mapDir != "") else name
    self.error=not(os.path.exists(self.path) and not(os.path.isdir(self.path)))

  def run(self):
    print self, self.error
    if(self.error): self.stop()

    while(not(self.exit)):
      data = plane.PlaneData(parser.parse(self.path), self.name)
      self.add(data)
     
  def stop(self):
    self.exit = True

class KinectSource(DataSource):
  name = "kinect-data"

  def __init__(self, queueMax = 3):
    super(KinectSource, self).__init__(queueMax)
    self.exit = False

    try: self.error = (freenect.sync_get_depth() is None)
    except: self.error = True

  def detect(self):
    detected = False
    try: detected = (freenect.sync_get_depth() is not None)
    except: pass

    self.error = not detected
    return detected

  def run(self):
    if(self.error): self.stop()

    while(not(self.exit)):
      try:
        data = freenect.sync_get_depth()
        if(data is None):
          self.stop()

        (data, _) = data
        data = plane.PlaneData(data.tolist(), KinectSource.name)
        self.add(data)
      except: pass

  def stop(self):
    freenect.sync_stop()
    self.exit = True
