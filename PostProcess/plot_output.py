import numpy as np
import matplotlib.pyplot as plt


# room and file input
baseFile = "../Output/SensorLog-"
fileType = ".csv"
out = "./"


# create plot styles for each room
numSensors = 4
# ps = ['--', 's-', 'x-', 'o:']
# ps = ['o', 's', 'x', '^']
ps = ['o--', 's-', 'x-', '^:']
msize = 3
mevery = 10
plotFED = 0


# expected csv column format:
#         |     (raw measured data)     |      (computed FED values)                | (computed hazard levels)  |
#   Time  | Temp  O2  CO  CO2 HCN Flux  | FED(Smoke)  FED(1st)  FED(2nd)  FED(3rd)  | Smoke     Burns     Fire  |  status


# get all the original data imported
time = []

FED_smoke = []
FED_pain = []
FED_incap = []
FED_fatal = []

Wsmoke = []
Wburn = []
Wfire = []

for i in range(0, numSensors):
  fileName = baseFile + str(i) + fileType
  A = np.loadtxt(fileName, delimiter=",")
  time.append(A[:,0])
  
  FED_smoke.append(A[:,7])
  FED_pain.append(A[:,8])
  FED_incap.append(A[:,9])
  FED_fatal.append(A[:,10])

  Wsmoke.append(A[:,11])
  Wburn.append(A[:,12])
  Wfire.append(A[:,13])


numRow = 3
numCol = 1
fig1, axes = plt.subplots(numRow, numCol, sharex=True, figsize=(5,7))

axes[0].set_title('Smoke Toxicity')
axes[1].set_title('Burn Threats')
axes[2].set_title('Fire Status')

# loop over all sensors
for i in range(0, numSensors):
  roomLabel = "Room " + str(i+1)  
  axes[0].plot( time[i], Wsmoke[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None' )  
  axes[1].plot( time[i], Wburn[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None'  )  
  axes[2].plot( time[i], Wfire[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None'  )

for ax in axes:
  ax.set_ylabel("Hazard Level")
  ax.set_xlim([0, 600])
  ax.set_ylim([0, 3.2])

axes[0].legend(loc = 2)
axes[-1].set_xlabel('Time [s]')

fig1.tight_layout()
fig1.savefig("output.pdf", dpi=600, format='pdf')
fig1.savefig("output.eps", dpi=600, format='eps')


if (plotFED == 1):
    numRow = 4
    numCol = 1
    fig2, axes = plt.subplots(numRow, numCol, sharex=True, figsize=(5,8))

    axes[0].set_title('FED Smoke')
    axes[1].set_title('FED Heat: Pain')
    axes[2].set_title('FED Heat: Injury')
    axes[3].set_title('FED Heat: Fatal')

    # loop over all sensors
    for i in range(0, numSensors):
      roomLabel = "Room " + str(i+1)  
      axes[0].plot( time[i], FED_smoke[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None' )  
      axes[1].plot( time[i], FED_pain[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None'  )  
      axes[2].plot( time[i], FED_incap[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None'  )
      axes[3].plot( time[i], FED_fatal[i], ps[i], ms=msize, markevery=mevery, label=roomLabel, markerfacecolor='None'  )


    FED_limit = np.ones((len(time[0]), 1))
    for ax in axes:
      ax.plot(time[0], FED_limit, color='grey', linestyle=':')
      ax.set_ylabel("Cumulative FED")
      ax.set_xlim([0, 600])
      ax.set_ylim([0, 2.0])

    axes[0].legend(loc = 2)
    axes[-1].set_xlabel('Time [s]')

    fig2.tight_layout()
    fig2.savefig("outFED.pdf", dpi=600, format='pdf')
    fig2.savefig("outFED.eps", dpi=600, format='eps')

plt.show()
