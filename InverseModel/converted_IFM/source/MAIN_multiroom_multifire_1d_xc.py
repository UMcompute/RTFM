# import statements
import time
import numpy as np
import matplotlib.pyplot as plt

# import other source files
import create_signal_xc
import read_signal_xc

#GLOBAL VALUES FOR CONFIG
numcomp = 4
numfire = 4    #numfire have to be smaller than numcomp, fire1 in comp1, fire2 in comp2, etc
numsignal = 8

#SCRIPT TO RUN WHOLE CODE
tic = time.time()
#----------------------------------------------------------------------------------------%

#INPUT DATA
#the format of data should be a matrix with [time1, hrr1, time2, hrr2...]
inData = np.loadtxt("../input/data4.txt")
mdata = inData.shape[0]
ndata = inData.shape[1]
hrrin = inData[:, 1:ndata]
timein = inData[:,0]
#print("size of hrrin is " + str(hrrin.shape[0]) + " by " + str(hrrin.shape[1]))
#print("length of timein is " + str(len(timein)))

#PLOT INITIAL HRR CURVES
plt.close('all')
f, axarr = plt.subplots(numfire, sharex=True)
for counter in range(0, numfire):
  print("create plot for fire #" + str(counter + 1))
  axarr[counter].plot(timein, hrrin[:, counter])
  if counter == numfire - 1:
    plt.xlabel('time')
  elif counter == 0:
    axarr[counter].set_title('hrr for forward model')
print("To show the initial HRR plots, uncomment #plt.show()")    
#plt.show()

#CREATE AND READ REAL CONCENTRATIONS AND FLOWS
create_signal_xc.create_signal_xc_func(timein, hrrin, numcomp, numfire, 'exp_signal_xc')
SIGNAL_exp = read_signal_xc.read_signal_xc_func(numcomp, 'exp_signal_xc')

#GET TIME FROM COLUMN 0; THEN DELETE IT FROM SIGNAL
TIME_exp = SIGNAL_exp[:, 0]
numTime = len(TIME_exp)
#print("size of SIGNAL_exp is " + str(SIGNAL_exp.shape[0]) + " by " + str(SIGNAL_exp.shape[1]))
SIGNAL_exp = np.delete(SIGNAL_exp, [0], axis=1)
#print("(post-delete) size of SIGNAL_exp is " + str(SIGNAL_exp.shape[0]) + " by " + str(SIGNAL_exp.shape[1]))

#INIALIZE VARIABLES
num_fail_allowed = 5
iteration_max = 20
error_tol = 0.001
error_max = 0.1
num_fail = 0
HRR_delta_base = 0.01
HRR_low = 5000.0
# Paul: we should rename k with something more descriptive
k = 1.0
k_avg = 0.0
HRR_max = 6.0 * 10.0 ** 5
HRR_min = 0.0
total_iteration = 0
low_tol = 0.001
extra_tol = 0.0
jump_tol = 1.0

#INITIALIZE ARRAYS
HRR_pred = 1000.0 * np.ones((numTime, numfire))
least_error = 100.0 * np.ones((numTime, 1))
#(for now signal is temperature)
SIGNAL_pred = 20.0 * np.ones((numTime, numsignal))
SIGNAL_turb = SIGNAL_pred
HRR_temp = 1000.0 * np.ones((1, numfire))
SIGNAL_lowfire = [0, 0, 0, 0]

# CHANGE 4 TO numTime FOR FINAL
for i in range(1, 4):
  print("Current Time = " + str(TIME_exp[i]))
  HRR_pred[i,:] = HRR_temp

  create_signal_xc.create_signal_xc_func(TIME_exp, HRR_pred, numcomp, numfire, 'pred_signal_xc')
  SIGNAL_pred = read_signal_xc.read_signal_xc_func(numcomp, 'pred_signal_xc')
  SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)
  #print("size of SIGNAL_pred is " + str(SIGNAL_pred.shape[0]) + " by " + str(SIGNAL_pred.shape[1]))

  # Paul: FOUND USE OF MAGIC NUMBERS == CHECK THIS SEGMENT (0:4)
  SIGNAL_diff = SIGNAL_pred[i,0:4] - SIGNAL_exp[i,0:4]
  max_SIGNAL_diff = max(abs(SIGNAL_diff))
  max_fire = np.argmax(abs(SIGNAL_diff))
  print("Max signal diff and max fire: " + str(max_SIGNAL_diff) + "  " + str(max_fire))

  least_error[i] = max_SIGNAL_diff
  iteration = 1
  HRR_new = 1000.0
  # Paul: we should rename factor with something more descriptive
  factor = 1.0

  while (max_SIGNAL_diff > error_tol):
    total_iteration += 1
    iteration += 1
    HRR_turb = HRR_pred

    # Paul: FOUND USE OF MAGIC NUMBER == CHECK THIS SEGMENT (25.0)
    # Paul: why is "iteration" in the denominator?
    HRR_delta = HRR_delta_base * HRR_pred[i, max_fire] * 25.0 / (25.0 + float(iteration))
    HRR_turb[i, max_fire] += HRR_delta

    create_signal_xc.create_signal_xc_func(TIME_exp, HRR_turb, numcomp, numfire, 'pred_signal_xc')
    SIGNAL_turb = read_signal_xc.read_signal_xc_func(numcomp, 'pred_signal_xc')
    SIGNAL_turb = np.delete(SIGNAL_turb, [0], axis=1)

    # Paul: FOUND MAGIC NUMBER (4)
    # Paul: check this (4) because it might be wrong in the 0-based Python indexing
    k1 = SIGNAL_turb[i, max_fire + int(SIGNAL_lowfire[max_fire] * 4)]
    k2 = SIGNAL_pred[i, max_fire + int(SIGNAL_lowfire[max_fire] * 4)]

    # Paul: WE NEED TO RENAME k TO SOMETHING MORE DESCRIPTIVE
    k = (k1 - k2) / HRR_delta

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
    create_signal_xc.create_signal_xc_func(TIME_exp, HRR_pred, numcomp, numfire, 'pred_signal_xc')
    SIGNAL_pred = read_signal_xc.read_signal_xc_func(numcomp, 'pred_signal_xc')
    SIGNAL_pred = np.delete(SIGNAL_pred, [0], axis=1)

    # Paul: FOUND USE OF MAGIC NUMBERS == CHECK THIS SEGMENT (0:4)
    SIGNAL_diff = SIGNAL_pred[i,0:4] - SIGNAL_exp[i,0:4]
    max_SIGNAL_diff = max(abs(SIGNAL_diff))
    max_fire = np.argmax(abs(SIGNAL_diff))
    print("Max signal diff and max fire: " + str(max_SIGNAL_diff) + "  " + str(max_fire))

    # terminate while loop early for testing
    max_SIGNAL_diff = 0.0

    '''
        #         if (HRR_pred(i-1,max_fire)<max(HRR_pred(i-1,:))/10.0 &&
        #         HRR_pred(i,max_fire)<0.6*max(HRR_pred(i-1,:)))
        if HRR_pred(i, max_fire) < 0.2 * (HRR_pred(i - 1, max_fire)) or (HRR_pred(i - 1, max_fire) < max(HRR_pred(i - 1, mslice[:])) * 0.1 and HRR_pred(i, max_fire) < 0.5 * max(HRR_pred(i - 1, mslice[:]))):
            SIGNAL_lowfire(max_fire).lvalue = 1
            HRR_low = max(0.2 * (HRR_pred(i - 1, max_fire)), max(HRR_pred(i - 1, mslice[:])) * 0.1)
            [tempmax_SIGNAL_diff, tempmax_fire] = max(abs(SIGNAL_diff) *elmul* (abs(HRR_pred(i, mslice[:])) > HRR_low))
            if tempmax_SIGNAL_diff > low_tol and SIGNAL_lowfire(max_fire) == 1 and max_SIGNAL_diff < jump_tol:
                max_SIGNAL_diff = tempmax_SIGNAL_diff
                max_fire = tempmax_fire


            end
        else:
            SIGNAL_lowfire(max_fire).lvalue = 0
        end

        max_SIGNAL_diff()
        if max_SIGNAL_diff < least_error(i):
            least_error(i).lvalue = max_SIGNAL_diff
            HRR_temp = HRR_pred(i, mslice[:])
        end

        if iteration > 0.5 * iteration_max:
            if (HRR_new < HRR_low) and (least_error(i) < low_tol):
                break
            elif (HRR_new > HRR_low) and (least_error(i) < extra_tol):
                break
            end
        end

        if iteration > iteration_max:
            if min(HRR_temp) < HRR_low:
                low_tol = min(least_error(i), error_max); print low_tol
            else:
                extra_tol = min(least_error(i), error_max); print extra_tol
            end

            if least_error(i) > error_max:
                num_fail = num_fail + 1; print num_fail
            end
            break
        end
        HRR_new = HRR_pred(i, max_fire)

    HRR_pred(i, mslice[:]).lvalue = HRR_temp
    if num_fail >= num_fail_allowed:
        break
    '''

# call timer function to finish main loop
toc = time.time()
tim = toc - tic;
print("total of " + str(tim) + " seconds elapsed")


'''
save(mstring('result.mat'), mstring('tim'), mstring('HRR_pred'), mstring('time'), mstring('total_iteration'), mstring('low_tol'), mstring('extra_tol'))

for counter in mslice[1:numfire]:
    #subplot(numfire+numsignal,2,counter*2)
    #     subplot(numfire+numsignal,2,counter*2-1)
    subplot(numfire, 1, counter)
    hold(mstring('on'))
    plot(time, HRR_pred(mslice[:], counter), mstring('r'))
    #     titlestr=sprintf('hrr for inverse model for fire %d',counter);
    #     title(titlestr)
    #     xlabel('time')
    #     ylabel('hrr')
end
hold(mstring('off'))
end
'''
