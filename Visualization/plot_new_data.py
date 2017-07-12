import matplotlib.pyplot as plt
import csv
import numpy as np

import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
	graph_data = open('example.txt', 'r').read()
	lines = graph_data.split('\n')
	xs = []
	ys = []
	for line in lines:
		if len(line) > 1:			# handle for empty line at the end
			x, y = line.split(',')		# delimiter is the comma
			xs.append(x)
			ys.append(y)
	ax1.clear()	
	ax1.plot(xs, ys)


# update every 1000 ms
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()



'''
print("Hello world!")

# 7 Loading Data from Files

x = []
y = []

with open('example.txt', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

x, y = np.loadtxt('example.txt', delimiter=',', unpack=True)
plt.plot(x, y, label='loaded from file')

plt.xlabel('input')
plt.ylabel('result')
plt.title('Updated Graph\nwith Labels')
plt.legend()
plt.show()
'''