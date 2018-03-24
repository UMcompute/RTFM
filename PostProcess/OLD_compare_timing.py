import matplotlib.pyplot as plt
import numpy as np


sensorList = [4, 8, 16, 32, 64, 128, 256, 512]
# sensorList = [4, 8, 16, 32]

fig, ax = plt.subplots(1, 1)

maxVals = []
avgVals = []
minVals = []

fileA = "send_time.csv"
fileB = "recv_time.csv"

outDir = "/mnt/c/Users/PaulA/Desktop/Journal-2/submission_02-01-18/data/OUT_600sec_error256/out-"

for s in sensorList:

  # dataDir = "../Testing/out-" + str(s) + "/"
  # dataDir = "../../../out-60SEC-test/out-" + str(s) + "/"

  dataDir = outDir + str(s) + "/"
  print(dataDir)

  A = np.loadtxt(dataDir + fileA, delimiter=",")
  B = np.loadtxt(dataDir + fileB, delimiter=",")

  x = B[:,0] - A[:,0]
  y = B[:,1] - A[:,1]
  z = B[:,2] - A[:,2]

  N = len(x)
  t = np.arange(1, N+1, 1)

  #=====
  # compute the time difference
  #  HH:MM:SS.ssssss
  #=====
  e = np.zeros(N)
  for i in range(0, N):
  	x[i] = float( x[i] / 3600.0 )
  	y[i] = float( y[i] / 60.0 )
  	e[i] = float( x[i] + y[i] + z[i] )

  a = np.mean(e, dtype=np.float64)
  f = a * np.ones(N)

  b = np.max(e)
  c = np.min(e)

  avgVals.append(a * 1000.0)  # convert to ms
  maxVals.append(b * 1000.0)  # convert to ms
  minVals.append(c * 1000.0)  # convert to ms

  # the error "e"  is in [sec]
  e_ms = 1000.0 * e
  f_ms = 1000.0 * f
  
  testName = str(s) + "-sensors"
  testNameAvg = testName + "-avg"
  ax.semilogy(t, e_ms, 'o-', label=testName)
  ax.semilogy(t, f_ms, '--', label=testNameAvg)

fig.legend(loc=2)


f2, ax2 = plt.subplots(1,1)

ax2.loglog(sensorList, avgVals, 'k-')
ax2.loglog(sensorList, maxVals, 'bx--')
ax2.loglog(sensorList, minVals, 'bo--')

# ax2.semilogx(sensorList, avgVals, 'k-')
# ax2.semilogx(sensorList, maxVals, 'bx--')
# ax2.semilogx(sensorList, minVals, 'bo--')

ax2.set_xlim([10**0,  10**3])
ax2.set_ylim([10**-1, 10**1])

ax2.set_xlabel("Number of Sensors")
ax2.set_ylabel("Computing Time per Measurement [ms]")

plt.show()
