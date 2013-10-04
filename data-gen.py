#!/usr/bin/python
import random
import math

# Set up constants
fileName = "data.csv"
dummyVal = 950.0

width = 640
height = 480

# User warning
print " -= WARNING! =-"
print "Will overwrite %s!" % (fileName)
raw_input("Continue?")

# Generate CSV data
lines = []
for x in xrange(width):
  temp = ""
  for y in xrange(height):
    # Simple periodic data
    val = math.sin(y/(2 * math.pi))*math.cos(x/(2 * math.pi)) + 1
    if(temp == ""):
      temp = str(val)
    else:
      temp += "," + str(val)

  if(lines == []):
    lines = [temp]
  else:
    lines += [temp]

# Write the CSV data to the file
f = open(fileName, 'r+')
f.seek(0)

for line in lines:
  f.write(line + "\n")

f.truncate()
f.close()
