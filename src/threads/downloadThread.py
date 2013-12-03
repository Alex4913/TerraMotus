import threading
import Queue
import time
import os

from src.tools import client

class Worker(threading.Thread):
  def __init__(self, dispRef):
    self.dispRef = dispRef
    self.mapDir = self.dispRef.mapDir
    self.imageDir = self.dispRef.imageDir

    self.client = client.Client(self.mapDir)
    threading.Thread.__init__(self)

  def genPlaceHolder(self):
    

  def run(self):
    try:
      
      self.client.getList("sorted")
    except:
