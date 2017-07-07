# import major modules 
import time
import numpy as np
import matplotlib.pyplot as plt

# import custom modules
import create_signal_xc
import read_signal_xc

#GLOBAL VALUES FOR CONFIG
NUMCOMP = 4
NUMFIRE = 4    #NUMFIRE must be <= NUMCOMP (fire1 in comp1, fire2 in comp2, etc)
NUMSIGNAL = 4

#DEFINE PATHS TO INPUT
dataFile = "../inp/data4.txt"

#CONSTANTS (in all CAPS)
NUM_FAILS_ALLOWED       = 20;
ITER_MAX                = 30;
ERROR_TOL               = 0.10;
ERROR_MAX               = 1.00;
HRR_LOW                 = 5000.0;
HRR_MAX                 = 6.0 * (10.0**5);

#SCRIPT TO RUN WHOLE CODE
tic = time.time()
#----------------------------------------------------------------------------------------%

#INPUT DATA

#the format of data should be a matrix with [timein, hrr1, hrr2, hrr3, hrr4]
inData = np.loadtxt(dataFile)
numStep = inData.shape[0]
numCols = inData.shape[1]
hrrin = inData[:, 1:numCols]
timein = inData[:,0]

#error handling: number of fires expected
if (numCols - 1 != NUMFIRE):
  print("\n***Input Error: check the data file " + dataFile + " to make sure it has one time column and then " + str(NUMFIRE) + " HRR columns.")
  exit()

#PLOT INITIAL HRR CURVES
plt.close('all')
f, axarr = plt.subplots(NUMFIRE, sharex=True)
for counter in range(0, NUMFIRE):
  axarr[counter].plot(timein, hrrin[:, counter], 'k-')
  if counter == NUMFIRE - 1:
    plt.xlabel('time')

#CREATE AND READ REAL CONCENTRATIONS AND FLOWS
create_signal_xc.create_signal_xc_func(timein, hrrin, NUMFIRE, 'exp_signal_xc')
SIGNAL_exp = read_signal_xc.read_signal_xc_func(NUMCOMP, 'exp_signal_xc')
TIME_exp = SIGNAL_exp[:, 0]  #GET TIME FROM COLUMN 0; THEN DELETE IT FROM SIGNAL
SIGNAL_exp = np.delete(SIGNAL_exp, [0], axis=1)

#INIALIZE VARIABLES
num_fail = 0
total_iteration = 0
error_low_tol = 0.01
error_extra_tol = 0.0

#INITIALIZE ARRAYS
HRR_pred = 1000.0 * np.ones((numStep, NUMFIRE))
error_least = 100.0 * np.ones(numStep)
SIGNAL_pred = 1.0 * np.ones((numStep, NUMSIGNAL))
HRR_temp = 1000.0 * np.ones((1, NUMFIRE))

#MAIN TIME LOOP
for i in range(1, numStep):
  print("Current Time = " + str(TIME_exp[i]))
  HRR_pred[i,:] = HRR_temp
  create_signal_xc.create_signal_xc_func(TIME_exp, HRR_pred, NUMFIRE, 'pred_signal_xc')
  SIGNAL_pred = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
  SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)
  SIGNAL_diff = SIGNAL_pred[i,:] - SIGNAL_exp[i,:]
  max_SIGNAL_diff = max(abs(SIGNAL_diff))
  max_fire = np.argmax(abs(SIGNAL_diff))
  error_least[i] = max_SIGNAL_diff
  iteration = 1
  factor = 1.0  # Paul: we should rename factor with something more descriptive

  #ITERATE TO GET NEW PREDICTION
  # Paul: MAGIC NUMBER 0.001
  error_new = SIGNAL_pred[i, max_fire] * 0.001
  while (max_SIGNAL_diff > max(ERROR_TOL, error_new)):
    print("iteration:  %2d   %.6f   %2d" % (iteration, max_SIGNAL_diff, max_fire+1))
    total_iteration += 1
    iteration += 1
    HRR_turb = HRR_pred

    # Paul: FOUND USE OF MAGIC NUMBERS 0.001, 1000.0
    HRR_delta = min(HRR_pred[i, max_fire] * 0.001, 1000.0)
    HRR_turb[i, max_fire] += HRR_delta
    
    create_signal_xc.create_signal_xc_func(TIME_exp, HRR_turb, NUMFIRE, 'pred_signal_xc')
    SIGNAL_turb = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
    SIGNAL_turb = np.delete(SIGNAL_turb, [0], axis=1)

    k = (SIGNAL_turb[i, max_fire] - SIGNAL_pred[i, max_fire]) / HRR_delta
    HRR_new = HRR_pred[i, max_fire] - SIGNAL_diff[max_fire] / k * factor

    # ***NOTE: k and HRR_new give different results than in MATLAB because of round-off errors

    if (HRR_new > HRR_MAX):
      HRR_new = HRR_MAX
      factor = 0.7 * factor                   # magic number
    else:
      factor = min(1.0, factor * 1.5)         # magic numbers

    HRR_pred[i, max_fire] = HRR_new
    create_signal_xc.create_signal_xc_func(TIME_exp, HRR_pred, NUMFIRE, 'pred_signal_xc')
    SIGNAL_pred = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
    SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)

    SIGNAL_diff = SIGNAL_pred[i,:] - SIGNAL_exp[i,:]
    max_SIGNAL_diff = max(abs(SIGNAL_diff))
    max_fire = np.argmax(abs(SIGNAL_diff))

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
    # end while loop

  print("iterations required = " + str(iteration))
  HRR_pred[i, :] = HRR_temp
  if num_fail >= NUM_FAILS_ALLOWED:
    break
  # end main time loop

# call timer function to finish main loop
toc = time.time()
tim = toc - tic;
print("\ntotal of " + str(tim) + " seconds elapsed")

# plot the results for the predicted HRR curve
for counter in range(0, NUMFIRE):
  #print("create plot for fire #" + str(counter + 1))
  axarr[counter].plot(TIME_exp, HRR_pred[:, counter], 'r-')
plt.show()