'''
hrr is is a matrix assigned as [hrr1,hrr2....]
numcomp is the number of compartment in use in the building, for now all
compartment is lined up as 6.1*4.9*2.4
numfire is the number of fires
all fire is burning at 3.05,2.45 of each building (fire 1 at the left 1st comp)
'''

import numpy as np
from shutil import copyfile
from os import system


def create_pred_signal_xc(time=None, hrr=None, numcomp=None, numfire=None):
  N = len(time)

  #For current purpose, we can just say the following data are all consistant
  SOOT = 0.01 + np.zeros(N)
  CO = 0.01 + np.zeros(N)
  TRACE = np.zeros(N)
  AREA = 1.0 + np.zeros(N)
  HEIGH = np.zeros(N)

  #Creting a .in file:
  copyfile('../input/Dalmarnocksetup.in', '../output/pred_signal_xc.in')
  fileNew = open('../output/pred_signal_xc.in', 'a') #NAME OF THE FILE
  # (appending to the end of the copied Dalmarnocksetup file)

  #This part will be modified with the num of fires
  #Current setting is fire 1 in comp 1, fire 2 in comp2, etc
  #And all fire are at (3.05,2.45) of the corresponding comp

  for counter in mslice[1:numfire]:
    fprintf(fileNew, mstring('!!\\r\\n'))
    fprintf(fileNew, mstring('!!Fire%d\\r\\n'), counter)    #%FIRE NAME
    fprintf(fileNew, mstring('FIRE,%d,1.5,2,0,1,TIME,0,0,0,0,Fire%d\\r\\n'), counter, counter)    #FIRE POSITION
    fprintf(fileNew, mstring('CHEMI,1,4,0,0,0,0.33,4.5E+07,METHANE\\r\\n'))    #FIRE TYPE
    fprintf(fileNew, mstring('TIME'))    #VECTOR TIME
    fprintf(fileNew, mstring(',%d'), time.cT)
    fprintf(fileNew, mstring('\\r\\nHRR'))    # VECTOR HRR
    fprintf(fileNew, mstring(',%d'), hrr(mslice[:], counter).cT)
    fprintf(fileNew, mstring('\\r\\nSOOT'))
    fprintf(fileNew, mstring(',%d'), SOOT)
    fprintf(fileNew, mstring('\\r\\nCO'))
    fprintf(fileNew, mstring(',%d'), CO)
    fprintf(fileNew, mstring('\\r\\nTRACE'))
    fprintf(fileNew, mstring(',%d'), TRACE)
    fprintf(fileNew, mstring('\\r\\nAREA'))
    fprintf(fileNew, mstring(',%d'), AREA)
    fprintf(fileNew, mstring('\\r\\nHEIGH'))
    fprintf(fileNew, mstring(',%d'), HEIGH)
  fileNew.close()

  #Run the file created and generate the excel spreadsheet that will be used
  #to read the predicted temperatures from:
  system('$CFAST ../output/pred_signal_xc')
  