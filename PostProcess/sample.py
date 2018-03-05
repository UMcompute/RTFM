import matplotlib.pyplot as plt
import numpy as np


t = np.arange(0.0, 600.0, 1.0)
s1 = np.sin(0.01 * np.pi * t)
s2 = 0.00001 * t * t
s3 = np.sin(0.05 * np.pi * t)

numRow = 3
numCol = 2

ylab = ["temp", "flux", "O2", "CO", "CO2", "HCN"]

# fig, axes = plt.subplots(numRow, numCol, sharex=True, figsize=(5,6))
fig, axes = plt.subplots(numRow, numCol, sharex=True)

k = 0
for i in range(0, numRow):
	for j in range(0, numCol):
		axes[i, j].plot(t, s1)
		axes[i, j].plot(t, s2)
		axes[i, j].plot(t, s3)
		axes[i, j].plot(t, s1 + s2 + s3)
		axes[i, j].set_ylabel(ylab[k])
		axes[i, j].set_title(ylab[k])
		k += 1

axes[2, 0].set_xlabel('Time [s]')
axes[2, 1].set_xlabel('Time [s]')

plt.tight_layout()
# plt.savefig("example.pdf", dpi=600, format='pdf')

plt.show()

