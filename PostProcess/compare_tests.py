import numpy as np
import matplotlib.pyplot as plt


outLoc = '/home/pbeata/results/'
outDirs = ['Output/', 
'Output_90sec/',
'Output_2xHRR/']


# room and file input
baseFile = "SensorLog-"
fileType = ".csv"


# create plot styles for each room
numSensors = 2
msize = 3
mevery = 10
ps = ['k-', 'b--', 'r:']
lab = ['(1) Original Test', 
'(2) 90-sec Ignition',
'(3) 2x Peak HRR']

# expected csv column format:
#         |     (raw measured data)     |      (computed FED values)                | (computed hazard levels)  |
#   Time  | Temp  O2  CO  CO2 HCN Flux  | FED(Smoke)  FED(1st)  FED(2nd)  FED(3rd)  | Smoke     Burns     Fire  |  status

numRow = 3
numCol = numSensors
fig1, axes = plt.subplots(numRow, numCol, sharex=True, figsize=(5,7))


k = 0
for out in outDirs:

	dataDir = outLoc + out 

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
		fileName = dataDir + baseFile + str(i) + fileType
		A = np.loadtxt(fileName, delimiter=",")
		time.append(A[:,0])

		FED_smoke.append(A[:,7])
		FED_pain.append(A[:,8])
		FED_incap.append(A[:,9])
		FED_fatal.append(A[:,10])

		Wsmoke.append(A[:,11])
		Wburn.append(A[:,12])
		Wfire.append(A[:,13])

		axes[0, i].set_title('Smoke Toxicity: Room ' + str(i+1) )
		axes[1, i].set_title('Burn Threats: Room ' + str(i+1) )
		axes[2, i].set_title('Fire Status: Room ' + str(i+1) )
		
		axes[-1, i].set_xlabel('Time [s]')

		axes[0, i].plot( time[i], Wsmoke[i], ps[k], ms=msize, markevery=mevery, label=lab[k], markerfacecolor='None' )  
		axes[1, i].plot( time[i], Wburn[i], ps[k], ms=msize, markevery=mevery, label=lab[k], markerfacecolor='None'  )  
		axes[2, i].plot( time[i], Wfire[i], ps[k], ms=msize, markevery=mevery, label=lab[k], markerfacecolor='None'  )

	k += 1


for i in range(0, numRow):
	for j in range(0, numCol):
		axes[i, j].set_xlim([0, 600])
		axes[i, j].set_ylim([0, 3.2])
		axes[i, 0].set_ylabel("Hazard Level")

axes[0, 0].legend(loc = 2)

fig1.tight_layout()

fig1.savefig("compare.pdf", dpi=600, format='pdf')
fig1.savefig("compare.eps", dpi=600, format='eps')

plt.show()

