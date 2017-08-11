import numpy as np


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



'''
Assumed DEVC file structure for n rooms:

HEADER LINE ROW 0: s C mol/mol mol/mol mol/mol mol/mol kW/m2 kW  C ... kW/m2 kW
HEADER LINE ROW 1: Time  T-1 O2-1  CO-1  CO2-1 HCN-1 Q-1 HRR-1 T-2 ... Q-n HRR-n
FIRST DATA ROW 2:  0.0 0.0 .................
'''

devcFile = "./data/methane_four_room_devc.csv"
numRowsHeader = 2
devcData = csvreadh_func(devcFile, numRowsHeader)
numInc = np.shape(devcData)[0]

numRooms = 4
numColsPerRoom = 7

fdsTime = devcData[:,0]
for i in range(0, numRooms):
  j1 = i * numColsPerRoom + 1
  j2 = j1 + numColsPerRoom 
  roomData = devcData[:, j1:j2]
  outFile = "file" + str(i) + ".csv"
  fw = open(outFile, 'w')
  for j in range(0, numInc):
    fw.write("%f" % roomData[j,0])
    # the -1 is so that it doesn't write HRR
    for k in range(1, numColsPerRoom-1):
      fw.write(",%f" % roomData[j,k])
    fw.write("\n")
  fw.close()
