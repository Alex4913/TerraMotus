import threading
import Queue
import time
import os

from src.tools import client

class Worker(threading.Thread):
  def __init__(self, mapDir, dataPlane, uploadButton):
    self.mapDir = mapDir
    self.dataPlane = dataPlane
    self.button = uploadButton
    self.done = False

    self.client = client.Client(self.mapDir)
    threading.Thread.__init__(self)

  def run(self):
    animation = Animate(self.button)
    animation.start()

    self.client = client.Client(self.mapDir)

    sent = False
    try:
      self.client.send(self.dataPlane.name)
      sent = True
    except:
      sent = False

    animation.stop()
    animation.validTransfer(sent)
    self.done = True

class Animate(threading.Thread):
  NO_BARS = "upload0.png"
  ONE_BAR = "upload1.png"
  MID_BARS = "upload2.png"
  HIGH_BARS = DEFAULT = "upload3.png"
  VALID = "upload4.png"
  INVALID = "upload5.png"

  tstep = 0.5

  def __init__(self, uploadButton):
    self.button = uploadButton
    self.exit = False
    threading.Thread.__init__(self)

  def cycleButton(self):
    tstep = Animate.tstep
    dt = time.time() - self.time
    if(dt <= tstep): self.button.setTexture(Animate.NO_BARS)
    elif(tstep < dt <= 2*tstep): self.button.setTexture(Animate.ONE_BAR)
    elif(2*tstep < dt <= 3*tstep): self.button.setTexture(Animate.MID_BARS)
    elif(3*tstep < dt <= 4*tstep): self.button.setTexture(Animate.HIGH_BARS)
    elif(4*tstep < dt <= 5*tstep): self.time = time.time()
 
  def validTransfer(self, valid):
    tstep = Animate.tstep
    if(valid):
      self.button.setTexture(Animate.VALID)
    else:
      self.button.setTexture(Animate.INVALID)
    
    time.sleep(3*tstep)
    self.button.setTexture(Animate.DEFAULT)

  def run(self):
    self.time = time.time()
    while(not(self.exit)):
      self.cycleButton()

  def stop(self):
    self.exit = True
