# this is the main script for getting updates from Ubuntu
import os
import time
import subprocess
import get_new_data

# input IP address and port of Linux machine
LINUX_IP = "141.212.44.209"
LINUX_PORT = "8080"
BASE_FILE = "room_"
FILE_TYPE = ".txt"
USE_LINUX = 1
NUM_ROOMS = 4

# timing constants
maxTime = 100.0
waitTime = 0.1

# =============================================================================
print("start main VISUALIZATION script")

# clear the data from the log files; launch live plots
fileNames = []
for i in range(0, NUM_ROOMS):
  open('temp_log_' + str(i) + '.txt', 'w').close()
  open('O2_log_' + str(i) + '.txt', 'w').close()
  open('CO_log_' + str(i) + '.txt', 'w').close()
  open('flux_log_' + str(i) + '.txt', 'w').close()
  # launch the live data plot subprocess
  command = 'python plot_live_data.py ' + str(i)
  subprocess.Popen(command, shell=True)
  fileNames.append("http://" + LINUX_IP + ":" + LINUX_PORT + "/" + BASE_FILE + str(i) + FILE_TYPE)

# pause for input
startMain = '0'
while (startMain == '0'):
  startMain = raw_input('Ready to start the simulation? (1 = yes)')

# download updates from the Linux machine
currTime = 0.0
while (currTime < maxTime) and (USE_LINUX == 1):
  currTime = currTime + waitTime
  time.sleep(waitTime)
  for i in range(0, NUM_ROOMS):
    get_new_data.download_updates(fileNames[i], i)
    print("downloaded new data %s" % fileNames[i])

# print confirmation that script finished
print "done with main script!"
