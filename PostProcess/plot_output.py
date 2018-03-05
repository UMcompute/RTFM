import numpy as np
import matplotlib.pyplot as plt


# room and file input
baseFile = "../Output/SensorLog-"
fileType = ".csv"
out = "./"


# create plot styles for each room
numSensors = 4
# ps = ['--', 's-', 'x-', 'o:']
ps = ['o', 's', 'x', '^']

# expected csv column format:
#         |     (raw measured data)     |      (computed FED values)        | (computed hazard levels)
#   Time  | Temp  O2  CO  CO2 HCN Flux  | FED(Smoke)  FED(Pain)  FED(Fatal) | Smoke     Burns     Fire 


# get all the original data imported
time = []
FED_smoke = []
FED_pain = []
FED_fatal = []
Wsmoke = []
Wburn = []
Wfire = []

for i in range(0, numSensors):
  fileName = baseFile + str(i) + fileType
  A = np.loadtxt(fileName, delimiter=",")
  FED_smoke.append(A[:,7])
  FED_pain.append(A[:,8])
  FED_fatal.append(A[:,9])
  Wsmoke.append(A[:,10])
  Wburn.append(A[:,11])
  Wfire.append(A[:,12])
FED_limit = np.ones((len(time[0]),1))


numRow = 3
numCol = 1
fig1, axes = plt.subplots(numRow, numCol, sharex=True, figsize=(6,8))


# loop over all sensors
for i in range(0, numSensors):
  roomLabel = "Room " + str(i+1)  

  ax3.plot( time[i], FED_smoke[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None' )
  ax4.plot( time[i], FED_pain[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )
  ax5.plot( time[i], FED_fatal[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None' )

  b1.plot( time[i], Wsmoke[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None' )  
  b2.plot( time[i], Wburn[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )  
  b3.plot( time[i], Wfire[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )


plt.show()
