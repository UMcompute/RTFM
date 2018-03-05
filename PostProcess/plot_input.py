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
# ps = ['o--', 's-', 'x-', '^:']

# expected csv column format:
#         |     (raw measured data)     |      (computed FED values)                | (computed hazard levels)  |
#   Time  | Temp  O2  CO  CO2 HCN Flux  | FED(Smoke)  FED(1st)  FED(2nd)  FED(3rd)  | Smoke     Burns     Fire  |  status


# Y axis limits
xx = [0.0, 600.0]
axisLimits = [ [0.0, 400.0],
[0.0, 8.0],
[14.0, 22.0],
[0.0, 10000.0],
[0.0, 4.0],
[0.0, 10.0] ]

# Y axis labels
axisLabels = [ '[$^{o}$C]', '[kW/m$^2$]', '[%]', '[ppm]', '[%]', '[ppm]' ]

# get all the original data imported
time = []
temp = []
flux = []
O2 = []
CO = []
CO2 = []
HCN = []
for i in range(0, numSensors):
  fileName = baseFile + str(i) + fileType
  A = np.loadtxt(fileName, delimiter=",")
  time.append(A[:,0])
  temp.append(A[:,1])
  O2.append(A[:,2])
  CO.append(A[:,3])
  CO2.append(A[:,4])
  HCN.append(A[:,5])
  flux.append(A[:,6])

# organize data for easy plotting
plotData = []
plotData.append(temp)
plotData.append(flux)
plotData.append(O2)
plotData.append(CO)
plotData.append(CO2)
plotData.append(HCN)

# ylab = ["Temperature", "Heat Flux", "O2", "CO", "CO2", "HCN"]
ylab = ["Temperature", "Heat Flux", "Oxygen ($O_{2}$)", "Carbon Monoxide ($CO$)", "Carbon Dioxide ($CO_{2}$)", "Hydrogen Cyanide ($HCN$)"]

numRow = 3
numCol = 2
fig, axes = plt.subplots(numRow, numCol, sharex=True, figsize=(5,7))


# loop over all sensors
count = 0
for i in range(0, numRow):
  for j in range(0, numCol):
    axes[i, j].set_title(ylab[count])
    axes[i, j].set_ylabel(axisLabels[count])
    axes[i, j].set_xlim(xx)
    axes[i, j].set_ylim(axisLimits[count])
    y = plotData[count]
    count += 1
    for k in range(0, numSensors):
      roomLabel = "Room " + str(k+1)
      axes[i, j].plot( time[k], y[k], ps[k], ms=3, markevery=8, label=roomLabel, markerfacecolor='None' )


axes[2, 0].set_xlabel('Time [s]')
axes[2, 1].set_xlabel('Time [s]')
axes[2, 1].legend(loc = 1)
axes[2, 1].text(30, 1, '(zero HCN in test)', style='italic')

plt.tight_layout()

plt.savefig("input.pdf", dpi=600, format='pdf')
#plt.savefig("input.eps", dpi=1000, format='eps')

plt.show()
