#! /usr/bin/python

# converts a run time over the given DISTANCE in meters to
# a minutes/mile pace

import sys

if len(sys.argv) != 4:
   print "usage: DISTANCE(m) MIN SEC"
   sys.exit()
   
dist = float(sys.argv[1])
sec = float(sys.argv[2]) * 60 + float(sys.argv[3])

pace = sec / (dist / 1609.34) # seconds per mile, 1609.34 m/mi

sec = int(round(pace % 60))
min = 0
while pace > 60:
   pace-=60
   min += 1

if sec < 10:
   s = "0"
else:
   s = ""

print "pace per mile: " + str(min) + ":" + s + str(sec)


