#!/usr/bin/python
import sys
import time

from src.threads import kinect, csvreader, engine, display
from src.tools import plane

###############################################################################
###                             Thread Init                                 ###
###############################################################################

def initCSVReader():
  print
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
  print
  print "Starting Kinect Thread"

  instance = kinect.Worker()
  instance.start()

  print " -> Checking for Kinect-ivity..."
  # Wait a tiny bit to ensure that the Kinect has been detected by now
  time.sleep(1)
  if(not(instance.kinectDetected)):
    print "   -> Not Found! Using CSVReader instead"
    instance.stop()
    return initCSVReader()
  print "   -> Found!"

  print " -> Waiting for initial data..."
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)
  print "   -> Got it!"

  return instance

def initPhysics(physicsQueue):
  print
  print "Starting Physics Engine"

  instance = engine.Worker(physicsQueue)
  print " -> Checking for data..."
  while(instance.dataPlane is None):
    time.sleep(0.100)
  print "   -> Got it!"

  print " -> Starting engine..."
  instance.start()
  print "   -> Choo choo, mothafucka!"

  return instance

def drawLogo():
  print
  print "          _____ "
  print "       .-'.  ':'-.       ______" 
  print "     .''::: .:    '.    /_  __/__ ___________ _"
  print "    /   :::::'      \    / / / -_) __/ __/ _ `/"
  print "   ;.    ':' `       ;  /_/__\\__/_/ /_/__\\_,_/"
  print "   |       '..       |    /  |/  /__  / /__ ______"
  print "   ; '      ::::.    ;   / /|_/ / _ \\/ __/ // (_-<"
  print "    \       '::::   /   /_/  /_/\\___/\\__/\\_,_/___/"
  print "     '.      :::  .'"
  print "       '-.___'_.-'"
  print

def init(args):
  if(("--help" in args) or ("-h" in args)):
    print "Usage:", args[0], "[options]"
    print "\t-h, --help\tPrint help information"
    print "\t-nk, --no-kinect\tSkip looking for a Kinect"
    exit()

  drawLogo()

  dataThread = None
  if(("--no-kinect" in args) or ("-nk" in args)): dataThread = initCSVReader()
  else:                                           dataThread = initKinect()

  physicsThread = initPhysics(dataThread.physicsQueue)

  return (dataThread, physicsThread)

def main():
  (dataThread, physicsThread) = init(sys.argv)

  print
  print "Starting Display"
  display.Worker(dataThread, physicsThread)

if(__name__ == "__main__"): main()
