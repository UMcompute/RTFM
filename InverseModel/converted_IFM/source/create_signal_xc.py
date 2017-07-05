"""
hrr is is a matrix assigned as [hrr1,hrr2....]
numcomp is the number of compartment in use in the building, for now all
compartment is lined up as 6.1*4.9*2.4 
numfire is the number of fires
all fire is burning at 3.05,2.45 of each building (fire 1 at the left 1st comp)
"""

import numpy as np
from shutil import copyfile
from os import system


def create_signal_xc_func(time=None, hrr=None, numcomp=None, numfire=None, inFile=None):
  N = len(time)

  #For current purpose, we can just say the following data are all consistant
  SOOT = 0.01 + np.zeros(N)
  CO = 0.01 + np.zeros(N)
  TRACE = np.zeros(N)
  AREA = 1.0 + np.zeros(N)
  HEIGH = np.zeros(N)

  #Creating the .in input file for CFAST:
  inpDir = '../input/'
  outDir = '../output/'
  baseFile = 'Dalmarnocksetup'
  file1 = inpDir + baseFile + '.in'
  file2 = outDir + inFile + '.in'
  copyfile(file1, file2)
  fileNew = open(file2, 'a') #NAME OF THE FILE
  # (appending to the end of the copied Dalmarnocksetup file)

  #This part will be modified with the num of fires
  #Current setting is fire 1 in comp 1, fire 2 in comp2, etc
  #And all fire are at (3.05,2.45) of the corresponding comp

  for counter in range(0, numfire):
    fileNew.write('!!\n')
    # FIRE NAME
    fileNew.write('!!Fire' + str(counter + 1) + '\n')
    # FIRE POSITION
    fileNew.write('FIRE,' + str(counter + 1) + ',1.5,2,0,1,TIME,0,0,0,0,Fire' + str(counter + 1) + '\n')
    #FIRE TYPE
    fileNew.write('CHEMI,1,4,0,0,0,0.33,4.5E+07,METHANE\n')
    
    # VECTOR TIME
    fileNew.write('TIME')
    for v in time:
      fileNew.write(", %.6f" % v)
    
    # VECTOR HRR
    fileNew.write('\nHRR')
    for v in hrr[:, counter]:
      fileNew.write(", %.6f" % v)
    
    # VECTOR SOOT  
    fileNew.write('\nSOOT')
    for v in SOOT:
      fileNew.write(", %.6f" % v)
    
    # VECTOR CO
    fileNew.write('\nCO')
    for v in CO:
      fileNew.write(", %.6f" % v)
    
    # VECTOR TRACE
    fileNew.write('\nTRACE')
    for v in TRACE:
      fileNew.write(", %.6f" % v)
    
    # VECTOR AREA
    fileNew.write('\nAREA')
    for v in AREA:
      fileNew.write(", %.6f" % v)
    
    # VECTOR HEIGH
    fileNew.write('\nHEIGH')
    for v in HEIGH:
      fileNew.write(", %.6f" % v)

  #close the new input file
  fileNew.close()

  #Run the file created and generate the excel spreadsheet that will be used
  #to read the predicted temperatures from:
  runFile = outDir + inFile
  sysText = '$CFAST ' + outDir + inFile
  system(sysText)
