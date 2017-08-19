import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


# get room number from command-line input argument
if (len(sys.argv) == 2):
  room = int(sys.argv[1])
else:
  print("***warning: expecting one command line argument for room number")

# initialize the figure with subplots
fig = plt.figure(figsize=(6, 4))
sub1 = fig.add_subplot(221)
sub2 = fig.add_subplot(222)
sub3 = fig.add_subplot(223)
sub4 = fig.add_subplot(224)

# define files to plot
file1 = 'temp_log_' + str(room) + '.txt'
file2 = 'O2_log_' + str(room) + '.txt'
file3 = 'CO_log_' + str(room) + '.txt'
file4 = 'flux_log_' + str(room) + '.txt'

# title above all the subplots
st = fig.suptitle("Live Data: Room " + str(room+1), fontsize="x-large")
ps = 'k-'

#====================================================================
def animate(i):
  tmax = 600.0

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
  sub1.plot(xs, ys, ps)
  sub1.set_xlim([0, tmax])
  sub1.set_ylim([0, 400])
  
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
  sub2.set_title('Oxygen')
  sub1.plot(xs, ys, ps)
  sub2.set_xlim([0, tmax])
  sub2.set_ylim([14, 22])

  # Carbon Monoxide Concentration
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
  sub3.set_title('Carbon Monoxide')
  sub1.plot(xs, ys, ps)
  sub3.set_xlim([0, tmax])
  sub3.set_ylim([0, 10000])

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
  sub1.plot(xs, ys, ps)
  sub4.set_xlim([0, tmax])
  sub4.set_ylim([0, 8])
#====================================================================


# update every 1000 ms (interval parameter)
ani = animation.FuncAnimation(fig, animate, interval=1000)

# shift subplots down:
plt.tight_layout()
st.set_y(0.95)
fig.subplots_adjust(top=0.85)
plt.show()
