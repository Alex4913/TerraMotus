import threading
import Queue

import libreenect

import time

class thread(threading.Thread):
  unfilteredData = None

  depthBounds = None
  noErrorData = None

  self.dataQueue = None

  def __init__(self, queue):
    self.dataQueue = queue
    threading.Thread.__init__(self)

    try:
      with noOut.noOut():
        

  def run(self):
    while
