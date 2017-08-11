# import major modules 
import time
import numpy as np
import matplotlib.pyplot as plt

# import custom modules
import create_signal_xc
import read_signal_xc

# included for LCM message passing
import lcm
import select
from send_to_ifm import data_to_ifm
from sent_by_ifm import data_from_ifm

global NUMCOMP


def my_handler(channel, data):
  msg = data_to_ifm.decode(data)
  print(msg.time_stamp)
  print(msg.temperature)
  print(msg.oxygen_conc)

  for i in range(0, NUMCOMP):
    # update temperature signal
    data_temperature.set_value(i, msg.temperature[i])
    # update oxygen concentration signal
    data_oxygen_conc.set_value(i, msg.oxygen_conc[i])

  data_temperature.set_time(msg.time_stamp)
  data_oxygen_conc.set_time(msg.time_stamp)


class Signal:

  def __init__(self):
    self.curr_time_stamp = 0.0
    self.curr_data = []
    for i in range(0, NUMCOMP):
      self.curr_data.append(0.0)

  def set_value(self, index, newValue):
    self.curr_data[index] = newValue

  def get_value(self, index):
    return self.curr_data[index]

  def set_time(self, newTime):
    self.curr_time_stamp = newTime

  def get_time(self):
    return self.curr_time_stamp


def my_format(value):
  return "%24.16f" % value


#GLOBAL VALUES FOR CONFIG
NUMCOMP = 4
NUMFIRE = 1    #NUMFIRE must be <= NUMCOMP (fire1 in comp1, fire2 in comp2, etc)
NUMDATA = 1
NUMSIGNAL = NUMDATA * NUMCOMP

#DEFINE PATHS TO INPUT
dataFile = "../inp/data4.txt"
#dataFile = "../inp/time_HRR_2.txt"

# MY CONTROL PARAMETERS
TESTING                 = 1
POLL_TIME               = 0.5
PLOTTING                = 1

#CONSTANTS (in all CAPS)
NUM_FAILS_ALLOWED       = 20
ITER_MAX                = 10
ERROR_TOL               = 0.20
ERROR_MAX               = 1.00
HRR_LOW                 = 10.0;
HRR_MAX                 = 6.0 * (10.0**5);

#SCRIPT TO RUN WHOLE CODE
tic = time.time()
#----------------------------------------------------------------------------------------%

# initialize the LCM library
if (TESTING == 0):
  lc = lcm.LCM()
  lc.subscribe("IFM_CHANNEL", my_handler)

#the format of data should be a matrix with [timein, hrr1, hrr2, hrr3, hrr4]
inData = np.loadtxt(dataFile)
numStep = inData.shape[0]
numCols = inData.shape[1]
hrrin = inData[:, 1:numCols]
timein = inData[:,0]

#CREATE AND READ REAL CONCENTRATIONS AND FLOWS
if (TESTING == 0):
  SIGNAL_exp = np.zeros((numStep,NUMSIGNAL))
  data_temperature = Signal()
  data_oxygen_conc = Signal()
else:
  create_signal_xc.create_signal_xc_func(timein, hrrin, NUMFIRE, 'exp_signal_xc')
  SIGNAL_exp = read_signal_xc.read_signal_xc_func(NUMCOMP, 'exp_signal_xc')
  TIME_exp = SIGNAL_exp[:, 0]  #GET TIME FROM COLUMN 0; THEN DELETE IT FROM SIGNAL
  SIGNAL_exp = np.delete(SIGNAL_exp, [0], axis=1)
  # initialize LCM data structure for sending back to MAIN
  ifm_output = data_from_ifm()
  ifm_output.num_fires = NUMFIRE
  ifm_output.current_HRR = 0.0

# INIALIZE VARIABLES
num_fail = 0
total_iteration = 0
error_low_tol = 0.01
error_extra_tol = 0.0

# INITIALIZE ARRAYS
HRR_pred = 100.0 * np.ones((numStep, NUMFIRE))
error_least = 100.0 * np.ones(numStep)
SIGNAL_pred = 1.0 * np.ones((numStep, NUMSIGNAL))
HRR_temp = 100.0 * np.ones((1, NUMFIRE))

#MAIN TIME LOOP: get sensor data using select function and waiting

''' LCM
i = 0
try:
  timeout = POLL_TIME  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()

      # increment the time step
      i += 1
      print("Current Time = %f" % data_temperature.get_time())

      # update SIGNAL_exp with LCM data
      for icomp in range(0, NUMCOMP):
        SIGNAL_exp[i, icomp] = data_temperature.get_value(icomp)
        SIGNAL_exp[i, icomp + NUMCOMP] = data_oxygen_conc.get_value(icomp)
'''

if (TESTING == 1):
  if (TESTING > 0):
    for i in range(1, 10):
      print("Current Time = %f" % timein[i])

      HRR_pred[i,:] = HRR_temp
      create_signal_xc.create_signal_xc_func(timein, HRR_pred, NUMFIRE, 'pred_signal_xc')
      SIGNAL_pred = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
      SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)
      SIGNAL_diff = SIGNAL_pred[i,:] - SIGNAL_exp[i,:]
      max_SIGNAL_diff = max(abs(SIGNAL_diff))
      max_fire = np.argmax(abs(SIGNAL_diff))

      if (max_fire >= NUMFIRE):
        max_fire = 0

      error_least[i] = max_SIGNAL_diff
      iteration = 1
      factor = 1.0    # Paul: we should rename "factor" with something more descriptive

      #ITERATE TO GET NEW PREDICTION
      error_new = SIGNAL_pred[i, max_fire] * 0.001    # Paul: MAGIC NUMBER 0.001
      while (max_SIGNAL_diff > max(ERROR_TOL, error_new)):
        print("iteration:  %2d   %.6f   %2d" % (iteration, max_SIGNAL_diff, max_fire+1))
        total_iteration += 1
        iteration += 1
        HRR_turb = HRR_pred
        HRR_delta = min(HRR_pred[i, max_fire] * 0.001, 1000.0)    # Paul: FOUND USE OF MAGIC NUMBERS 0.001, 1000.0
        HRR_turb[i, max_fire] += HRR_delta

        create_signal_xc.create_signal_xc_func(timein, HRR_turb, NUMFIRE, 'pred_signal_xc')
        SIGNAL_turb = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
        SIGNAL_turb = np.delete(SIGNAL_turb, [0], axis=1)

        k = (SIGNAL_turb[i, max_fire] - SIGNAL_pred[i, max_fire]) / HRR_delta   
        # Paul: we should rename "k" with something more descriptive
        HRR_new = HRR_pred[i, max_fire] - SIGNAL_diff[max_fire] / k * factor    
        
        # ***NOTE: k could be zero! Need to handle this error

        # ***NOTE: k and HRR_new give different results than in MATLAB,
        #       presumably because of round-off errors (check this)

        if (HRR_new > HRR_MAX):
          HRR_new = HRR_MAX
          factor = 0.7 * factor                   # magic number
        else:
          factor = min(1.0, 1.5 * factor)         # magic numbers
        HRR_pred[i, max_fire] = HRR_new

        create_signal_xc.create_signal_xc_func(timein, HRR_pred, NUMFIRE, 'pred_signal_xc')
        SIGNAL_pred = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
        SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)
        SIGNAL_diff = SIGNAL_pred[i,:] - SIGNAL_exp[i,:]
        max_SIGNAL_diff = max(abs(SIGNAL_diff))
        max_fire = np.argmax(abs(SIGNAL_diff))

        if (max_fire >= NUMFIRE):
          max_fire = 0

        if max_SIGNAL_diff < error_least[i]:
          error_least[i] = max_SIGNAL_diff
          HRR_temp = HRR_pred[i,:]

        checkDum = float(iteration) > (0.5 * float(ITER_MAX))
        if (checkDum == True):
          checkVal = 1.0
        else:
          checkVal = 0.0
        check1 = HRR_new < HRR_LOW
        check2 = error_least[i] < 0.5 * (error_low_tol + checkVal)
        check3 = HRR_new > HRR_LOW
        check4 = error_least[i] < 0.5 * (error_extra_tol + checkVal)
        if (check1 and check2) or (check3 and check4):
          break

        if (iteration >= ITER_MAX):
          HRR_pred[i,:] = HRR_temp
          if min(HRR_temp) < HRR_LOW:
            error_low_tol = min(error_least[i], ERROR_MAX)
          else:
            error_extra_tol = min(error_least[i], ERROR_MAX)
          if (error_least[i] > ERROR_MAX):
            num_fail += 1
          break

        # print the output
        np.savetxt('HRR1.out', HRR_pred, delimiter=',', fmt='%f')
        # end while loop

      print("iterations required = " + str(iteration))
      HRR_pred[i, :] = HRR_temp
      if num_fail >= NUM_FAILS_ALLOWED:
        break


''' LCM
      # send HRR back to MAIN
      for ifire in range(0, NUMFIRE):
        ifm_output.current_HRR[ifire] = HRR_pred[i,ifire]
      lc.publish("IFM_OUT_CHANNEL", ifm_output.encode())

      # end main time loop
    else:
      print("\n   [waiting for msg in IFM main loop]")
except KeyboardInterrupt:
  pass
'''


# call timer function to finish main loop
toc = time.time()
tim = toc - tic;
print("\ntotal of " + str(tim) + " seconds elapsed")

# print the output
np.savetxt('../out/HRR1.out', HRR_pred, delimiter=',', fmt='%f')

# plot the results for the predicted HRR curve
if (PLOTTING == 1):
  plt.close('all')
  if (NUMFIRE == 1):
    fig1, ax = plt.subplots()
    ax.plot(timein, hrrin[:,0])
    ax.plot(timein, HRR_pred[:,0])
    ax.set_title('sample title')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('HRR [kW]')
    fig1.tight_layout()
  else:
    fig2, axall = plt.subplots(NUMFIRE, sharex=True)
    for i in range(0, NUMFIRE):
      axall[i].plot(timein, hrrin[:,i])
      axall[i].plot(timein, HRR_pred[:,i])
    fig2.tight_layout()
  plt.show()
