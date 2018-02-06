from shutil import copyfile

uniqueSensors = 4
targetSensors = 24

key = 0
for i in range(0, targetSensors):
  if (i >= uniqueSensors):
    src = "file" + str(key) + ".csv"
    dst = "file" + str(i) + ".csv"
    copyfile(src, dst)
    print( "copied %s to %s" % (src, dst) )
  if (key < uniqueSensors-1):
    key += 1
  else:
    key = 0

print("\n[TOTAL OF %d SENSORS AVAILABLE VIA REPEATED DATA]\n" % targetSensors)
