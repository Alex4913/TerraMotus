#!/usr/bin/python
import sys
import time

from src.threads import kinect, csvreader, engine, display
from src.tools import plane

###############################################################################
###                             Thread Init                                 ###
###############################################################################

PLANE = "tilt"

# Simple method to both print and append to a log file (with timestamp)
def log(message):
  logFile = "log.log"
  f = open(logFile, "a+")
  output = time.strftime("[%x, %X]") + ": " + message
  print output
  f.write(output + "\n")
  f.close()

def initCSVReader():
  mapDir = "maps"
  log("Emulating Kinect with CSVReader Thread")
  instance = csvreader.Worker(mapDir)
  instance.setPlaneName(PLANE)

  if(not(instance.fileExists)):
    log("No data in " + instance.planeName + "! Aborting.")
    instance.stop()
    exit()

  log("Reading in CSV")
  instance.start()
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)
  return instance

def initKinect():
  log("Starting Kinect Thread")

  instance = kinect.Worker()
  instance.setPlaneName(PLANE)
  instance.start()

  log("Checking for Kinect-ivity")
  # Wait a tiny bit to ensure that the Kinect has been detected by now
  time.sleep(1)
  if(not(instance.kinectDetected)):
    log("Not Found! Using CSVReader instead")
    instance.stop()
    return initCSVReader()

  log("Waiting for initial data")
  while(instance.physicsQueue.empty() or instance.graphicsQueue.empty()):
    time.sleep(0.100)

  return instance

def initPhysics(physicsQueue):
  log("Starting Physics Engine")

  instance = engine.Worker(physicsQueue)
  log("Checking for data")
  while(instance.dataPlane is None):
    time.sleep(0.100)

  log("Starting engine")
  instance.start()

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

  log("Starting display")
  display.Worker(dataThread, physicsThread)
  log("Exiting")

if(__name__ == "__main__"): main()
