# import statements
import time
import numpy as np
import matplotlib.pyplot as plt

# import other source files
import create_exp_signal_xc
import read_exp_signal_xc

#GLOBAL VALUES FOR CONFIG
numcomp = 4
numfire = 4  #numfire have to be smaller than numcomp, fire1 in comp1, fire2 in comp2, etc
numsignal = 8

#SCRIPT TO RUN WHOLE CODE
tic = time.time()
#----------------------------------------------------------------------%

#INPUT VARIABLES
#the format of data should be a matrix with [time1, hrr1, time2, hrr2...]
inputPath = '../input/data4.mat'
#str = strcat(mstring('data4.mat'))
#str=strcat('C:\Users\Xiaolin Cai\Desktop\research1\multiroom_multifire\data.mat');

#a = load(inputPath)
data = np.loadtxt("../input/data4.txt")

mdata = data.shape[0]
ndata = data.shape[1]

#hrrin = a.hrr
hrrin = data[:, 1:ndata]
print("size of hrrin is " + str(hrrin.shape[0]) + " by " + str(hrrin.shape[1]))

#timein = a.t
timein = data[:,0]
print("length of timein is " + str(len(timein)))

#plot forward model
# for counter = 1:numfire
#     subplot(numfire+numsignal,2,counter*2-1)   %Only plot for temperature and hrr for now
#     plot(timein,hrrin(:,counter))
#     titlestr=sprintf('hrr for forward model for fire %d',counter);
#     title(titlestr)
#     xlabel('time')
#     ylabel('hrr')

plt.close('all')
f, axarr = plt.subplots(numfire, sharex=True)
for counter in range(0, numfire):
  print("create plot for fire #" + str(counter + 1))
  axarr[counter].plot(timein, hrrin[:, counter])
  if counter == numfire - 1:
    plt.xlabel('time')
  elif counter == 0:
    axarr[counter].set_title('hrr for forward model')
#plt.show()


# 05-31-17 DISABLED FUNCTION CALLS FOR NOW
'''
create_exp_signal_xc(timein, hrrin, numcomp, numfire)#function that creates the 'real concentrations and flows'
[time, SIGNAL_exp] = read_exp_signal_xc(numcomp)#function that reads the 'real concentrations'
'''
# 05-31-17 DISABLED FUNCTION CALLS FOR NOW


create_exp_signal_xc.create_exp_signal_xc_func(timein, hrrin, numcomp, numfire)
SIGNAL_exp = read_exp_signal_xc.read_exp_signal_xc_func(numcomp)
TIME_exp = SIGNAL_exp[:, 0]


num_fail_allowed = 5
iter_max = 20
#iter_turn=20;
error_tol = 0.001
error_max = 0.1


n = len(TIME_exp)
HRR_pred = np.zeros((n, numfire)) + 1000.0
least_error = np.zeros((n, 1)) + 100.0
SIGNAL_pred = np.zeros((n, numsignal)) + 20.0  #For now signal is temperature
SIGNAL_turb = SIGNAL_pred
num_fail = 0
#error_extra = 0
HRR_delta_base = 0.01
HRR_low = 5000.0
#HRR_delta_lowhrr = 50000


k = 1.0
factor = 1.0
HRR_max = 6.0 * 10.0 ** 5
HRR_min = 0.0
total_iter = 0
low_tol = 0.001
extra_tol = 0.0
jump_tol = 1.0
k_avg = 0.0
HRR_temp = np.zeros((1, numfire)) + 1000.0
SIGNAL_lowfire = [0, 0, 0, 0]


for i in range(1, n):
  HRR_pred[i,:] = HRR_temp

  create_pred_signal_xc(time, HRR_pred, numcomp, numfire)
  read_pred_signal_xc(numcomp)
  
  SIGNAL_diff = SIGNAL_pred(i, mslice[1:4]) - SIGNAL_exp(i, mslice[1:4])
  [max_SIGNAL_diff, max_fire] = max(abs(SIGNAL_diff))
  least_error(i).lvalue = max_SIGNAL_diff
  iter = 1
  HRR_new = 1000
  lag = 0
  factor = 1


'''
    while max_SIGNAL_diff > error_tol:


        total_iter += 1
        iter = iter + 1; print iter
        HRR_turb = HRR_pred
        HRR_delta = HRR_delta_base * HRR_pred(i, max_fire) * 25.0 / (25.0 + iter)
        HRR_turb(i, max_fire).lvalue = HRR_turb(i, max_fire) + HRR_delta

        create_pred_signal_xc(time, HRR_turb, numcomp, numfire)
        read_pred_signal_xc(numcomp)
        k = (SIGNAL_turb(i, max_fire + SIGNAL_lowfire(max_fire) * 4) - SIGNAL_pred(i, max_fire + SIGNAL_lowfire(max_fire) * 4)) / HRR_delta
        #         if k>0
        #             k_avg=(k_avg*(i-1)/i+k/i);
        #         elseif HRR_new<HRR_low && k<0
        #             k=k_avg;
        #         end

        HRR_new = HRR_pred(i, max_fire) - SIGNAL_diff(max_fire) / k * factor    #get new hrr

        if (HRR_new > HRR_max):
            HRR_new = HRR_max
            factor = 0.5 * factor
        elif (HRR_new < HRR_min):
            HRR_new = 0.1 * max(HRR_pred(i - 1, mslice[:]))
            factor = 0.5 * factor
        else:
            factor = min(1, factor * 1.5)
        end

        HRR_pred(i, max_fire).lvalue = HRR_new
        create_pred_signal_xc(time, HRR_pred, numcomp, numfire)
        read_pred_signal_xc(numcomp)
        SIGNAL_diff = SIGNAL_pred(i, mslice[1:4]) - SIGNAL_exp(i, mslice[1:4])
        [max_SIGNAL_diff, max_fire] = max(abs(SIGNAL_diff)); print max_SIGNAL_diff; print max_fire    #update signal &signal_diff

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

        if iter > 0.5 * iter_max:
            if (HRR_new < HRR_low) and (least_error(i) < low_tol):
                break
            elif (HRR_new > HRR_low) and (least_error(i) < extra_tol):
                break
            end
        end

        if iter > iter_max:
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



    end
    HRR_pred(i, mslice[:]).lvalue = HRR_temp
    if num_fail >= num_fail_allowed:
        break
    end
'''


toc = time.time()
tim = toc - tic;
print("total of " + str(tim) + " seconds elapsed")


'''
save(mstring('result.mat'), mstring('tim'), mstring('HRR_pred'), mstring('time'), mstring('total_iter'), mstring('low_tol'), mstring('extra_tol'))

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
