"""
# This function will read 
#1. the vctor of time
#2. the matrix of vectors of firesignal over time [signal1, signal2,
#signal3,...]

#Inputs:  Number of Cpompartments, Number of Fire- Will get the concentration values from an excel spreadsheet
#Outputs: The vector of time simulation
#         The matrix of fire signal 
"""


import numpy as np
import csvreadh


def read_signal_xc_func(numcomp=None, inFile=None):
  # setting config
  #If use upper layer temperature, use 1, else, 0
  #If use O2 concentration, use 1, else, 0
  #If use CO2 concentration, use 1, else, 0
  #If use Mass flow rate, use 1, else, 0
  #If use upper layer volume, use 1, else, 0
  usedsignal = [0, 0, 0, 0, 1]

  # (replaces magic number)
  HT_DIMENSION = 2.45

  #According to Guo's paper, temperature turns out to be the best fire temperature.
  # Paul: What does this mean? Temp is the best predictor maybe? 

  #if other fire signal is used, this part has to change
  #numsignal = usedsignal[0] * numcomp + usedsignal[1] * numcomp + usedsignal[2] * numcomp 
  
  #For each compartment, it'll have one upper layer temperature, O2 concentration, CO2 concentration
  numsignal = 0
  for i in range(0, len(usedsignal)):
    numsignal += usedsignal[i] * numcomp

  # starting column of signalData matrix
  column = 0

  #Read the time vector and length
  outDir = '../out/'
  filename = outDir + inFile + '_n.csv'
  csvData = csvreadh.csvreadh_func(filename)
  time = csvData[:, 0]
  numSteps = len(time)
  signalData = np.zeros((numSteps, numsignal + 1))

  # store time in first column of signalData output
  signalData[:, column] = time
  column += 1
  
  # signal for temperature
  if usedsignal[0] == 1:
    for i in range(0, numcomp):
      # get column id
      j = (5 * i + 1)
      signalData[:, column] = csvData[:, j]
      column += 1

  # signal for O2 concentration
  if usedsignal[1] == 1:
    filename = outDir + inFile + '_s.csv'
    csvData = csvreadh.csvreadh_func(filename)    
    for i in range(0, numcomp):
      # get column id
      j = (20 * i + 2)
      signalData[:, column] = csvData[:, j]
      column += 1

  # signal for CO2 concentration
  if usedsignal[2] == 1:
    if usedsignal[1] == 0:
      filename = outDir + inFile + '_s.csv'
      csvData = csvreadh.csvreadh_func(filename)
    for i in range(0, numcomp):
      # get column id
      j = (20 * i + 3)
      signalData[:, column] = csvData[:, j]
      column += 1

  # signal for mass flow rate
  if usedsignal[3] == 1:
    filename = outDir + inFile + '_f.csv'
    csvData = csvreadh.csvreadh_func(filename)
    for i in range(0, numcomp):
      # get column id
      j = (2 * i + 3)
      signalData[:, column] = csvData[:, j]
      column += 1

  # signal for upper layer volume
  if usedsignal[4] == 1:
    filename = outDir + inFile + '_n.csv'
    csvData = csvreadh.csvreadh_func(filename)
    layerHeight = np.zeros((numSteps, numcomp))
    tempUpper = np.zeros((numSteps, numcomp))
    tempLower = np.zeros((numSteps, numcomp))
    for i in range(0, numcomp):
      # locate upper layer volume in csv
      j1 = (5 * i + 3)
      layerHeight[:, i] = csvData[:, j1]
      # locate upper layer temp in csv
      j2 = (5 * i + 1)
      tempUpper[:, i] = csvData[:, j2]
      # locate lower layer temp in csv
      j3 = (5 * i + 2)
      tempLower[:, i] = csvData[:, j3]
    # USES ELEMENT-WISE ARRAY MULTIPLICATION HERE:
    tempSignal = (HT_DIMENSION - layerHeight) * tempUpper 
    tempSignal += layerHeight * tempLower
    for i in range(0, numcomp):
      signalData[:, column] = tempSignal[:, i]
      column += 1

  return signalData