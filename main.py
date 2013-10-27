#!/usr/bin/python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
import time

from src.threads import kinect, csvreader, engine
from src.tools import plane

def initCSVReader():
  print "Emulating Kinect with CSVReader Thread"
  instance = csvreader.Worker()

  if(not(instance.fileExists)):
    print " -> No data in " + instance.fileName + "! Aborting."
    instance.stop()
    exit()

  print " -> Reading in CSV"
  instance.start()
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)
  print "   -> Got it!"
  return instance

def initKinect():
  print "Starting Kinect Thread"

  instance = kinect.Worker()
  instance.start()

  print " -> Checking for Kinect-ivity..."
  startTime = time.time()
  while(not(instance.kinectDetected) and time.time() - startTime <= 5):
    time.sleep(0.100)

  if(not(instance.kinectDetected)):
    print "   -> Not Found! Using CSVReader instead"
    time.sleep(0.1)
    instance.stop()
    return initCSVReader()
  print "   -> Found!"

  print " -> Waiting for initial data..."
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)
  print "   -> Got it!"

  return instance

def initPhysics(physicsQueue):
  print "Starting Physics Engine"

  instance = engine.Worker(physicsQueue)
  print " -> Checking for data..."
  while(not(instance.dataPlaneUpdated)):
    continue
  print "   -> Got it!"

  print " -> Starting engine..."
  instance.start()
  print "   -> Choo choo!"

  return instance

def init():
  print "         _____ "
  print "      .-'.  ':'-.       ______" 
  print "    .''::: .:    '.    /_  __/__ ___________ _"
  print "   /   :::::'      \    / / / -_) __/ __/ _ `/"
  print "  ;.    ':' `       ;  /_/__\\__/_/ /_/__\\_,_/"
  print "  |       '..       |    /  |/  /__  / /__ ______"
  print "  ; '      ::::.    ;   / /|_/ / _ \\/ __/ // (_-<"
  print "   \       '::::   /   /_/  /_/\\___/\\__/\\_,_/___/"
  print "    '.      :::  .'"
  print "      '-.___'_.-'"
  print

  dataThread = initKinect()
  physicsThread = initPhysics(dataThread.physicsQueue)

  return (dataThread, physicsThread)

def main():
  (dataThread, physicsThread) = init()
  print "Waiting in Main!"
  while(True):
    try:
      time.sleep(0.1)
    except KeyboardInterrupt:
      print
      print "Caught kill signal!"
      break

  for thread in (dataThread, physicsThread):
    thread.stop()

main()