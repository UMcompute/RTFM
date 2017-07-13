import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


# initialize the figure with subplots
fig = plt.figure(figsize=(6, 4))
sub1 = fig.add_subplot(221)
sub2 = fig.add_subplot(222)
sub3 = fig.add_subplot(223)
sub4 = fig.add_subplot(224)

# choose files to plot
testing_plots = 0
if testing_plots == 1:
  file1 = 'sample_temp_2.txt'
  file2 = 'sample_O2_2.txt'
  file3 = 'sample_HRR_2.txt'
  file4 = 'sample_flux_2.txt'
else:
  file1 = 'temp_log.txt'
  file2 = 'o2_log.txt'
  file3 = 'hrr_log.txt'
  file4 = 'flux_log.txt'

# title above all the subplots
st = fig.suptitle("Live Data: Room 1", fontsize="x-large")


#====================================================================
def animate(i):
  tmax = 120.0

  # Temperature
  graph_data = open(file1, 'r').read()
  lines = graph_data.split('\n')
  xs = []
  ys = []
  for line in lines:
    if len(line) > 1:           # handle for empty line at the end
      x, y = line.split(',')    # delimiter is the comma
      xs.append(x)
      ys.append(y)
  sub1.clear()
  sub1.set_title('Temperature')
  sub1.plot(xs, ys)
  sub1.set_xlim([0, tmax])
  sub1.set_ylim([0, 600])
  
  # Oxygen Concentration
  graph_data = open(file2, 'r').read()
  lines = graph_data.split('\n')
  xs = []
  ys = []
  for line in lines:
    if len(line) > 1:           # handle for empty line at the end
      x, y = line.split(',')    # delimiter is the comma
      xs.append(x)
      ys.append(y)  
  sub2.clear()
  sub2.set_title('Oxygen Concentration')
  sub2.plot(xs, ys)
  sub2.set_xlim([0, tmax])
  sub2.set_ylim([0, 100])

  # Heat Release Rate
  graph_data = open(file3, 'r').read()
  lines = graph_data.split('\n')
  xs = []
  ys = []
  for line in lines:
    if len(line) > 1:           # handle for empty line at the end
      x, y = line.split(',')    # delimiter is the comma
      xs.append(x)
      ys.append(y)  
  sub3.clear()
  sub3.set_title('Heat Release Rate')
  sub3.plot(xs, ys)
  sub3.set_xlim([0, tmax])
  sub3.set_ylim([0, 5000])

  # Heat Flux
  graph_data = open(file4, 'r').read()
  lines = graph_data.split('\n')
  xs = []
  ys = []
  for line in lines:
    if len(line) > 1:           # handle for empty line at the end
      x, y = line.split(',')    # delimiter is the comma
      xs.append(x)
      ys.append(y)
  sub4.clear()
  sub4.set_title('Heat Flux')
  sub4.plot(xs, ys)
  sub4.set_xlim([0, tmax])
  sub4.set_ylim([0, 50])
#====================================================================


# update every 1000 ms (interval parameter)
ani = animation.FuncAnimation(fig, animate, interval=1000)

# shift subplots down:
plt.tight_layout()
st.set_y(0.95)
fig.subplots_adjust(top=0.85)
plt.show()