from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy

import freenect

import time
import math

from src.threads.resources import buttons
from src.threads.frames import sim, main, loading

class Worker(object):
  frameName = "-= TerraMotus =-"
  width = 1080
  height = 720
  frameSize = (width, height)

  clearColor = (1, 1, 1, 1)

  # Milliseconds
  updateDelay = 42

  def preGL(self):
    glShadeModel(GL_FLAT)

  def postGL(self):
    glutSwapBuffers()
  
  def timerFired(self, value):
    self.currentFrame.timerFired(value)

  def parseMainButtons(self):
    if(main.MainMenu.PLAY in self.main.buttonsPressed):
      self.sim.pause(False)
      self.currentFrame = self.sim
    elif(main.MainMenu.DOWNLOAD in self.main.buttonsPressed):
      print "Download Menu!"
    elif(main.MainMenu.ABOUT in self.main.buttonsPressed):
      print "About Menu!"
      

  def parseSimButtons(self):
    if(sim.Simulation.HOME in self.sim.buttonsPressed):
      self.sim.pause(True)
      self.currentFrame = self.main
    elif(sim.Simulation.UPLOAD in self.sim.buttonsPressed):
      print "Upload Interface!"

  def parseButtonPress(self):
    if(self.currentFrame == self.main): self.parseMainButtons()
    elif(self.currentFrame == self.sim): self.parseSimButtons()

  def mouse(self, mouseButton, buttonState, x, y):
    if(buttonState == GLUT_DOWN):
      self.currentFrame.mouse(mouseButton, buttonState, x, y)
      self.parseButtonPress()

  def keyboard(self, key, x, y):
    self.currentFrame.keyboard(key, x, y)

  def specialKeys(self, key, x, y):
    self.currentFrame.specialKeys(key, x, y)

  def draw(self):
    self.preGL()
    self.currentFrame.draw()
    self.postGL()

  def close(self):
    freenect.sync_stop()

  def runGL(self):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(*Worker.frameSize)
    glutCreateWindow(Worker.frameName)
  
    glutDisplayFunc(self.draw)
    glutIdleFunc(self.draw)
    glutTimerFunc(Worker.updateDelay, self.timerFired, 0)
    glutMouseFunc(self.mouse)
    glutKeyboardFunc(self.keyboard)
    glutSpecialFunc(self.specialKeys)
    glutCloseFunc(self.close)

    # Blocks
    glutMainLoop()
   
  def __init__(self, dataThread, physicsThread):
    self.dataThread = dataThread
    self.physicsThread = physicsThread

    self.sim = sim.Simulation(Worker.frameSize, dataThread, physicsThread)
    self.main = main.MainMenu(Worker.frameSize)
    self.loading = loading.Loading(Worker.frameSize)
    self.currentFrame = self.main

    self.runGL()
