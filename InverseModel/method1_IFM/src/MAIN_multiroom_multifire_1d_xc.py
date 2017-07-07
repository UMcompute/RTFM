# import major modules 
import time
import numpy as np
#import matplotlib.pyplot as plt

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
HRR_DELTA_BASE          = 0.01;
HRR_LOW                 = 5000.0;
HRR_DELTA_LOW           = 50000.0;
HRR_MAX                 = 6.0 * (10.0**5);
HRR_MIN                 = -300000.0;
HRR_JUMP_TOL            = 3.0;
FACTOR_LOW              = 0.7;
FACTOR_HI               = 1.2;

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

'''
#PLOT INITIAL HRR CURVES
plt.close('all')
f, axarr = plt.subplots(NUMFIRE, sharex=True)
for counter in range(0, NUMFIRE):
  #print("create plot for fire #" + str(counter + 1))
  axarr[counter].plot(timein, hrrin[:, counter], 'k-')
  if counter == NUMFIRE - 1:
    plt.xlabel('time')
  #elif counter == 0:
  #  axarr[counter].set_title('hrr for forward model')
#print("To show the initial HRR plots, uncomment #plt.show()")    
#plt.show()
'''

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
testTime = 3    # ***REPLACE testTime with numStep in the main for loop
for i in range(1, testTime):
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
  print("iteration:  %2d   %.6f   %2d" % (iteration, max_SIGNAL_diff, max_fire+1))

  '''   LINE-BY-LINE UPDATE IN PROGRESS
  while (max_SIGNAL_diff > error_tol):
    total_iteration += 1
    iteration += 1
    HRR_turb = HRR_pred

    # Paul: FOUND USE OF MAGIC NUMBER == CHECK THIS SEGMENT (25.0)
    # Paul: why is "iteration" in the denominator?
    HRR_delta = HRR_delta_base * HRR_pred[i, max_fire] * 25.0 / (25.0 + float(iteration))
    HRR_turb[i, max_fire] += HRR_delta

    create_signal_xc.create_signal_xc_func(TIME_exp, HRR_turb, NUMCOMP, NUMFIRE, 'pred_signal_xc')
    SIGNAL_turb = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
    SIGNAL_turb = np.delete(SIGNAL_turb, [0], axis=1)

    # Paul: FOUND MAGIC NUMBER (4)
    # Paul: check this (4) because it might be wrong in the 0-based Python indexing
    k1 = SIGNAL_turb[i, max_fire + int(SIGNAL_lowfire[max_fire] * 4)]
    k2 = SIGNAL_pred[i, max_fire + int(SIGNAL_lowfire[max_fire] * 4)]

    # Paul: WE NEED TO RENAME k TO SOMETHING MORE DESCRIPTIVE
    k = (k1 - k2) / HRR_delta

    #print("%.6f" % HRR_delta)
    #print("k1, k2, k = %.8f %.8f %.8f" % (k1, k2, k))

    # Get new HRR
    HRR_new = HRR_pred[i, max_fire] - SIGNAL_diff[max_fire] / k * factor
    if (HRR_new > HRR_max):
      HRR_new = HRR_max
      factor = 0.5 * factor                   # magic number
    elif (HRR_new < HRR_min):
      HRR_new = 0.1 * max(HRR_pred[i-1, :])   # magic number
      factor = 0.5 * factor                   # magic number
    else:
      factor = min(1.0, factor * 1.5)         # magic numbers

    HRR_pred[i, max_fire] = HRR_new
    create_signal_xc.create_signal_xc_func(TIME_exp, HRR_pred, NUMCOMP, NUMFIRE, 'pred_signal_xc')
    SIGNAL_pred = read_signal_xc.read_signal_xc_func(NUMCOMP, 'pred_signal_xc')
    SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)

    # Paul: FOUND USE OF MAGIC NUMBERS == CHECK THIS SEGMENT (0:4)
    SIGNAL_diff = SIGNAL_pred[i,0:4] - SIGNAL_exp[i,0:4]
    max_SIGNAL_diff = max(abs(SIGNAL_diff))
    max_fire = np.argmax(abs(SIGNAL_diff))

    #print("iteration:  %2d   %.6f   %2d" % (iteration, max_SIGNAL_diff, max_fire+1))
    #print("Max signal diff and max fire: " + str(max_SIGNAL_diff) + "  " + str(max_fire))

    # Paul: FOUND MAGIC NUMBERS 0.2, 0.1, 0.5
    check1 = HRR_pred[i, max_fire]   <  0.2 * HRR_pred[i-1, max_fire]
    check2 = HRR_pred[i-1, max_fire] <  0.1 * max(HRR_pred[i-1, :])
    check3 = HRR_pred[i, max_fire]   <  0.5 * max(HRR_pred[i-1, :])

    if check1 or (check2 and check3):
      SIGNAL_lowfire[max_fire] = 1
      # Paul: magic numbers 0.2, 0.1
      HRR_low = max(0.2 * HRR_pred[i-1, max_fire], 0.1 * max(HRR_pred[i-1, :]))
      check_HRR = np.zeros(NUMFIRE)
      for j in range(0, NUMFIRE):
        if abs(HRR_pred[i, j]) > HRR_low:
          check_HRR[j] = 1.0
      tempmax_SIGNAL_diff = max(abs(SIGNAL_diff) * check_HRR)
      tempmax_fire = np.argmax(abs(SIGNAL_diff) * check_HRR)
      if (tempmax_SIGNAL_diff > low_tol) and (SIGNAL_lowfire[max_fire] == 1) and (max_SIGNAL_diff < jump_tol):
        max_SIGNAL_diff = tempmax_SIGNAL_diff
        max_fire = tempmax_fire
    else:
      SIGNAL_lowfire[max_fire] = 0

    #print("iteration:  " + str(iteration) + '  ' + str(max_SIGNAL_diff) + '  ' + str(max_fire+1))
    print("iteration:  %2d   %.6f   %2d" % (iteration, max_SIGNAL_diff, max_fire+1))

    if (max_SIGNAL_diff < least_error[i]):
      least_error[i] = max_SIGNAL_diff
      HRR_temp = HRR_pred[i, :]

    # Paul: MAGIC NUMBER 0.5
    if iteration > 0.5 * iteration_max:
      if (HRR_new < HRR_low) and (least_error[i] < low_tol):
        break
      elif (HRR_new > HRR_low) and (least_error[i] < extra_tol):
        break

    if iteration > iteration_max:
      if min(HRR_temp) < HRR_low:
        low_tol = min(least_error[i], error_max)
      else:
        extra_tol = min(least_error[i], error_max)

      if least_error[i] > error_max:
        num_fail += 1
      break
    HRR_new = HRR_pred[i, max_fire]

  # end while loop
  print("iterations required = " + str(iteration))
  HRR_pred[i, :] = HRR_temp
  if num_fail >= num_fail_allowed:
    break

# plot the results for the predicted HRR curve
for counter in range(0, NUMFIRE):
  #print("create plot for fire #" + str(counter + 1))
  axarr[counter].plot(TIME_exp, HRR_pred[:, counter], 'r-')
plt.show()
'''

# call timer function to finish main loop
toc = time.time()
tim = toc - tic;
print("\ntotal of " + str(tim) + " seconds elapsed")
