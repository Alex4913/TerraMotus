#!/usr/bin/python
import os
import stat
import sys
import time

from src.threads import display

# Simple method to both print and append to a log file (with timestamp)
def log(message, logFile = "log.log"):
  """
  Log a message to the end of a log file

  Keyword Arguments:
  message -- the message to append
  logFile -- the relative path to the log file (default "log.log")
  """

  f = open(logFile, "a+")
  output = time.strftime("[%x, %X]") + ": " + message
  print output
  f.write(output + "\n")
  f.close()

def createDirs(dirs):
  """
  Create directories from a list of paths

  Keyword Arguments:
  dirs -- list of paths of folders to be created
  """

  for folder in dirs:
    if(not(os.path.exists(folder)) and not(os.path.isdir(folder))):
      # Make the folder and give it the correct properties (RWX)
      os.mkdir(folder)
      os.chmod(folder, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

def drawLogo():
  # Draw a cool logo!
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
  """
  Init functions

  Keyword Arguments:
  args -- Program runtime arguments
  """

  # Display a
  if(("--help" in args) or ("-h" in args)):
    print "Usage:", args[0], "[options]"
    print "\t-h, --help\tPrint help information"
    print "\t-nk --no-kinect\tSkip looking for a Kinect"
    exit()

  drawLogo()

def main():
  """
  Main function called at runtime.

  Init program, create folders and initialize display
  """

  init(sys.argv)

  mapDir = "maps"
  imageDir = "images"
  resourceDir = "resources"
  createDirs((mapDir, imageDir, resourceDir))

  # Create a display
  log("Starting display")
  display.Worker(mapDir, imageDir, resourceDir, sys.argv)

# Run the main function if this class is called to be run, and not imported
if(__name__ == "__main__"): main()
