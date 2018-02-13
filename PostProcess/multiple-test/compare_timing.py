import matplotlib.pyplot as plt
import numpy as np


sensorList = [4, 8, 16, 32, 64, 128, 256, 512]
# sensorList = [4, 8, 16, 32]

fig, ax = plt.subplots(1, 1)

avgVals = []

for s in sensorList:

  dataDir = "../../Testing/out-" + str(s) + "/"
  # dataDir = "../../../out-60SEC-test/out-" + str(s) + "/"

  fileA = "send_time.csv"
  fileB = "recv_time.csv"

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

  avgVals.append(a * 1000.0)  # convert to ms

  # the error "e"  is in [sec]
  e_ms = 1000.0 * e
  f_ms = 1000.0 * f
  
  testName = str(s) + "-sensors"
  testNameAvg = testName + "-avg"
  ax.semilogy(t, e_ms, 'o-', label=testName)
  ax.semilogy(t, f_ms, '--', label=testNameAvg)

fig.legend(loc=2)


f2, ax2 = plt.subplots(1,1)
ax2.semilogx(sensorList, avgVals, 'ko-')
ax2.set_xlabel("Number of Sensors")
ax2.set_ylabel("Average Computing Time per Measurement [ms]")

plt.show()
