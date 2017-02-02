import subprocess
import time
import os
import signal

# used for LCM to establish listener
import select
import lcm
from fromSensor import sensor


def my_handler(channel, data):
    msg = sensor.decode(data)
    print("\nMAIN Received message on channel \"%s\"" % channel)
    print("   time = %s" % str(msg.time))
    print("   temp = %s" % str(msg.temp))
    print("   flux = %s" % str(msg.flux))
    print("\n")


print("this is the start of main.py")

# initialize the LCM library
lc = lcm.LCM()
lc.subscribe("SENSOR", my_handler)

# launch main menu for user
print("\nMain Menu: ")
answer = '2'
while answer == '2':
  answer = raw_input('Start new sensor? (1/0) ')
  if answer == '1':
    sensorDir = raw_input('what is the sensor directory? ')
    sensorName = raw_input('what is the sensor source code name? ')
  elif answer == '0':
    print('no sensor will be used!')
  else:
    print("***error: please enter only 1 (yes) or 0 (no)");
    answer = '2'

# can python run the Makefile of a c++ app for us too?
# (or maybe do this in a bash script instead)

# requires that we know where the sensor is located
#sensorDir = '/home/pbeata/Research/FireMonitoring/SENSORS/3_RemoteRepoSSH/'

# requires this application be compiled first
#sensorName = 'SimpleSensor.exe'   

# start the single sensor for dev mode at beginning of Main program only
print("\n***warning for testing: ignoring main menu and using 1 pre-defined sensor")
dataName = 'FDS_FirstMin.dat'
sensorDir = './fromSensors/'
sensorName = 'sensor.exe' + ' ' + sensorDir + dataName 
fullExePath = sensorDir + sensorName

# start subprocess for the sensor program
p = subprocess.Popen("exec " + fullExePath, shell=True)

# try to implement select example from LCM
try:
    timeout = 0.5  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()
        else:
            print("Waiting for messages...")
except KeyboardInterrupt:
    pass

# assume some calculations take 3 seconds
print("\nsleep for 3 seconds... then kill proc")
time.sleep(3)

# kill the sensor program
x = p.kill()
print("**TRIED TO KILL the sensor subprocess! (but cannot confirm it)")

print("this is the end of main.py")
