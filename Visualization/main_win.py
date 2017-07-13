# this is the main script for getting updates from Ubuntu
import os
import time
import subprocess
import get_new_data

# input IP address and port of Linux machine
LINUX_IP = "141.212.44.237"
LINUX_PORT = "8080"
DATA_FILE = "new_data.txt"
USE_LINUX = 1

# timing constants
maxTime = 80.0
waitTime = 0.5

# =============================================================================
print("start main VISUALIZATION script")

# clear the data from the log files
open('temp_log.txt', 'w').close()
open('o2_log.txt', 'w').close()
open('hrr_log.txt', 'w').close()
open('flux_log.txt', 'w').close()

# launch the live data plot subprocess
command = 'python plot_live_data.py'
subprocess.Popen(command, shell=True)

# pause for input
startMain = raw_input('Ready to start the simulation? ')

# download updates from the Linux machine
currTime = 0.0
fileName = "http://" + LINUX_IP + ":" + LINUX_PORT + "/" + DATA_FILE
while (currTime < maxTime) and (USE_LINUX == 1):
  currTime = currTime + waitTime
  time.sleep(waitTime)
  get_new_data.download_updates(fileName)
  print("downloaded new data %s \n" % DATA_FILE)

# print confirmation that script finished
print "done with main script!"









#os.system("http-server -o")

# files used in live plots
#logFiles = ['temp_log.txt', 'flux_log.txt']
#logFiles = ['sample_temp_1.txt', 'sample_flux_1.txt', 'sample_O2_1.txt']
#logFiles = ['sample_temp_2.txt', 'sample_flux_2.txt', 'sample_O2_2.txt', 'sample_HRR_2.txt']

# plot live data coming computing workstation
'''
pid_array = []
for file in logFiles:
  command = 'python plot_new_data.py ' + file
  pid_array.append(subprocess.Popen(command, shell=True))

print("continue with rest of script")
'''

# clear the log files before downloading new data
'''
fw1 = open('temp_log.txt', 'w')
fw2 = open('o2_log.txt', 'w')
fw3 = open('hrr_log.txt', 'w')
fw4 = open('flux_log.txt', 'w')
fw1.close()
fw2.close()
fw3.close()
fw4.close()
'''


'''
# kill the live plots
for pid in pid_array:
  print("*warning: killing pid of a live plot")
  pid.kill()
'''
# sample "status.txt" file 
'''
wait
0, 0, 0, 0
'''

# user input: start monitoring? 
# start: 1

# user input: which models to include? 
# SENSOR: 0 or 1
# EDM: 0 or 1
# IFM: 0 or 1
# AAA: 0 or 1

# sample of the updated "status.txt" file 
'''
start
1, 1, 1, 1
'''

  #print("downloaded " + DATA_FILE + " at " + str(currTime) + " seconds")
