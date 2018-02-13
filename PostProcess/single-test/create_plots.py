import numpy as np
import matplotlib.pyplot as plt


# room and file input
baseFile = "../Output/SensorLog-"
fileType = ".csv"
out = "./"


# create plot styles for each room
numSensors = 4
ps = ['--', 's-', 'x-', 'o:']

# numSensors = 32
# ps = 8 * ['--', 's-', 'x-', 'o:']


# expected csv column format:
#         |     (raw measured data)     |      (computed FED values)        | (computed hazard levels)
#   Time  | Temp  O2  CO  CO2 HCN Flux  | FED(Smoke)  FED(Pain)  FED(Fatal) | Smoke     Burns     Fire 


# axis limits
tmin = 0.0
tmax = 300.0

tempMax = 400.0
fluxMax = 8.0
O2max = 22.0
O2min = 14.0
CO2max = 4.0
COmax = 10000.0
HCNmax = 100.0


# get all the original data imported
allData = []
nsteps = []
time = []

temp = []
flux = []

O2 = []
CO = []
CO2 = []
HCN = []

FED_smoke = []
FED_pain = []
FED_fatal = []

Wsmoke = []
Wburn = []
Wfire = []

for i in range(0, numSensors):
  fileName = baseFile + str(i) + fileType
  A = np.loadtxt(fileName, delimiter=",")
  allData.append(A)
  nsteps.append(np.shape(A)[0])
  time.append(A[:,0])
  temp.append(A[:,1])
  O2.append(A[:,2])
  CO.append(A[:,3])
  CO2.append(A[:,4])
  HCN.append(A[:,5])
  flux.append(A[:,6])
  FED_smoke.append(A[:,7])
  FED_pain.append(A[:,8])
  FED_fatal.append(A[:,9])
  Wsmoke.append(A[:,10])
  Wburn.append(A[:,11])
  Wfire.append(A[:,12])
FED_limit = np.ones((nsteps[0],1))



# init figures
f1, (ax1, ax2) = plt.subplots(1, 2)
f2, (ax3, ax4, ax5) = plt.subplots(3, 1, sharex=True)
f3, (ax6, ax7, ax8) = plt.subplots(3, 1, sharex=True)
f4, (b1, b2, b3) = plt.subplots(3, 1, sharex=True)


# set a title for each data set
ax1.set_title('Upper Layer Gas Temperature')
ax2.set_title('Radiative Heat Flux')

ax3.set_title('FED Smoke Toxicity')
ax4.set_title('FED Heat: Pain')
ax5.set_title('FED Heat: Fatality')

ax6.set_title('Oxygen')
ax7.set_title('Carbon Dioxide')
ax8.set_title('Carbon Monoxide')

b1.set_title('Smoke Toxicity')
b2.set_title('Burn Threats')
b3.set_title('Fire Status')



# loop over all sensors
for i in range(0, numSensors):
  roomLabel = "Room " + str(i+1)  

  ax1.plot( time[i], temp[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None')
  ax2.plot( time[i], flux[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None' )

  ax3.plot( time[i], FED_smoke[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )
  ax4.plot( time[i], FED_pain[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )
  ax5.plot( time[i], FED_fatal[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )

  ax6.plot( time[i], O2[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )
  ax7.plot( time[i], CO2[i], ps[i], ms=5, markevery=5, label=roomLabel, markerfacecolor='None'  )
  ax8.plot( time[i], CO[i], ps[i], ms=5, markevery=5, label=
    roomLabel, markerfacecolor='None'  )

  b1.plot( time[i], Wsmoke[i], ps[i], ms=5, markevery=5, label=
    roomLabel, markerfacecolor='None'  )  
  b2.plot( time[i], Wburn[i], ps[i], ms=5, markevery=5, label=
    roomLabel, markerfacecolor='None'  )  
  b3.plot( time[i], Wfire[i], ps[i], ms=5, markevery=5, label=
    roomLabel, markerfacecolor='None'  )  

ax1.set_ylabel('Temperature [$^\circ$C]')
ax1.set_xlabel('Time [$s$]')
ax1.set_xlim([tmin, tmax])
ax1.set_ylim([0.0, tempMax])

# ax2.legend(loc=2)
ax2.set_ylabel('Heat Flux [$kW/m^2$]')
ax2.set_xlabel('Time [$s$]')
ax2.set_xlim([tmin, tmax])
ax2.set_ylim([0.0, fluxMax])

# ax3.legend(loc=2)
ax3.plot( time[0], FED_limit, color='grey', linestyle=':' )
ax3.set_ylim([0.0, 2.0])
ax3.set_xlim([tmin, tmax])

ax4.plot( time[0], FED_limit, color='grey', linestyle=':' )
ax4.set_ylim([0.0, 2.0])
ax4.set_xlim([tmin, tmax])

ax5.plot( time[0], FED_limit, color='grey', linestyle=':' )
ax5.set_ylim([0.0, 2.0])
ax5.set_xlim([tmin, tmax])

ax6.set_xlim([tmin, tmax])
ax6.set_ylim([O2min, O2max])

ax7.set_xlim([tmin, tmax])
ax7.set_ylim([0.0, CO2max])

ax8.set_xlim([tmin, tmax])
ax8.set_ylim([0.0, COmax])

b1.set_xlim([tmin, tmax])
b1.set_ylim([0.0, 3.0])

b2.set_xlim([tmin, tmax])
b2.set_ylim([0.0, 3.0])

b3.set_xlim([tmin, tmax])
b3.set_ylim([0.0, 3.0])



# SAVE FIGURES TO PDF FORMAT

f1.tight_layout()
f1.savefig(out + 'temp-flux.pdf', format='pdf', dpi=600)

f2.tight_layout()
f2.savefig(out + 'FED.pdf', format='pdf', dpi=600)

f3.tight_layout()
f3.savefig(out + 'concentrations.pdf', format='pdf', dpi=600)

f4.tight_layout()
f4.savefig(out + 'warnings.pdf', format='pdf', dpi=600)

plt.show()
