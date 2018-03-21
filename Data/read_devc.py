import numpy as np
from shutil import copyfile


#==========================================================
# two data files used in the journal paper:
# CASE 1
devcFile = "../Data/propane_two_fire_devc.csv"
# CASE 2
#devcFile = "../Data/propane_two_fire_90sec_devc.csv"
#==========================================================


# A function to read data from the FDS-produced devc file:
def csvreadh_func(filename=None, numRowsHeader=0):
  my_data = np.genfromtxt(filename, delimiter=',')
  mrows = np.shape(my_data)[0] 
  ncols = np.shape(my_data)[1]
  dataMat = np.zeros((mrows - numRowsHeader, ncols))
  rownum = 0
  for row in my_data:
    if rownum >= numRowsHeader:
      colnum = 0
      for v in row:
        dataMat[rownum - numRowsHeader][colnum] = v
        colnum += 1
    rownum += 1
  return dataMat


# If NUM_SENSORS > (# of unique sensors), 
# then copy the data files:
def copy_data(uniqueSensors=0, targetSensors=0, dataDir=None):
  key = 0
  print(" ");
  for i in range(0, targetSensors):
    if (i >= uniqueSensors):
      src = dataDir + "file" + str(key) + ".csv"
      dst = dataDir + "file" + str(i) + ".csv"
      copyfile(src, dst)
      # print( "copied %s to %s" % (src, dst) )
    if (key < uniqueSensors-1):
      key += 1
    else:
      key = 0


'''
Assumed DEVC file structure for n rooms:

HEADER LINE ROW 0: s C mol/mol mol/mol mol/mol mol/mol kW/m2 kW  C ... kW/m2 kW
HEADER LINE ROW 1: Time  T-1 O2-1  CO-1  CO2-1 HCN-1 Q-1 HRR-1 T-2 ... Q-n HRR-n
FIRST DATA ROW 2:  0.0 0.0 .................

(we do not write the Time column to our sensor files)
'''

# open the input file to read the number of rooms/sensors needed
dataDir = "../Data/"
inputFile = "../Exec/input.txt"
fr = open(inputFile, 'r')
NUM_SENSORS = int( fr.readline() )
fr.close()

# ASSUMPTIONS (SEE ABOVE FORMAT AND CHECK FDS DEVC FILE)
numColsPerRoom = 7
numRoomsOrig = 4
numRowsHeader = 2

# read the FDS output to get time-series data for RTFM
devcData = csvreadh_func(devcFile, numRowsHeader)
numInc = np.shape(devcData)[0]
fdsTime = devcData[:,0]
for i in range(0, numRoomsOrig):
  j1 = i * numColsPerRoom + 1
  j2 = j1 + numColsPerRoom 
  roomData = devcData[:, j1:j2]
  outFile = dataDir + "file" + str(i) + ".csv"
  fw = open(outFile, 'w')
  for j in range(0, numInc):
    fw.write("%f" % roomData[j,0])
    # the -1 is so that it doesn't write HRR
    for k in range(1, numColsPerRoom-1):
      fw.write(",%f" % roomData[j,k])
    fw.write("\n")
  fw.close()

# IF WE ARE USING MORE THAN FOUR ROOMS, WE NEED TO COPY DATA:
if (NUM_SENSORS > numRoomsOrig):
  copy_data(numRoomsOrig, NUM_SENSORS, dataDir)
print("\n[UNIQUE SENSOR DATA FILES: %d]" % numRoomsOrig)
print("\n[TOTAL OF %d SENSOR FILES AVAILABLE]\n" % NUM_SENSORS)
