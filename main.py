#!/usr/bin/python
import os
import stat
import sys
import time

from src.threads import display

###############################################################################
###                             Thread Init                                 ###
###############################################################################

# Simple method to both print and append to a log file (with timestamp)
def log(message):
  logFile = "log.log"
  f = open(logFile, "a+")
  output = time.strftime("[%x, %X]") + ": " + message
  print output
  f.write(output + "\n")
  f.close()

def createDirs(dirs):
  for folder in dirs:
    if(not(os.path.exists(folder)) and not(os.path.isdir(folder))):
      os.mkdir(folder)
      os.chmod(folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

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

def main():
  init(sys.argv)

  mapDir = "maps"
  imageDir = "images"
  resourceDir = "resources"
  createDirs((mapDir, imageDir, resourceDir))

  log("Starting display")
  display.Worker(mapDir, imageDir, resourceDir, sys.argv)

if(__name__ == "__main__"): main()
