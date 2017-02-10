import subprocess
import time
import os
import signal

# used for LCM to establish listener
import select
import lcm
from fromSensor import sensor

# used for LCM to establish sender
from toIFM import ifm
from toEDM import edm


def my_handler(channel, data):
    msg = sensor.decode(data)
    print("\nMAIN.py Received message on channel \"%s\"" % channel)
    print("   time = %s" % str(msg.time))
    print("   temp = %s" % str(msg.temp))
    print("   flux = %s" % str(msg.flux))
    print("\n")
    global currTime
    global currTemp
    global currFlux
    currTime = msg.time
    currTemp = msg.temp
    currFlux = msg.flux


# ===================================================================
# START THE MAIN PROGRAM LOOP

print("this is the start of main.py")

# initialize the LCM library
lc = lcm.LCM()
lc.subscribe("SENSOR", my_handler)


# ===================================================================
# LAUNCH SENSOR WITH FIRE DATA FILE

# launch main menu for user
# todo: include kill process option in menu for user to kill sensor
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
sensorProc = subprocess.Popen("exec " + fullExePath, shell=True)


# start subprocess for IFM
ifmStart = 'python IFM_main.py'
ifmProc = subprocess.Popen("exec " + ifmStart, shell=True)


# ===================================================================
# START RECEIVER TO GET SENSOR DATA INTO MAIN LOOP

# get sensor data using select function and waiting
try:
    timeout = 0.5  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()

            # distribute data to the running subprocess models

            # send to IFM
            msgForIFM = ifm()
            msgForIFM.time = currTime
            msgForIFM.temp = currTemp
            msgForIFM.flux = currFlux
            lc.publish("IFM_CHAN", msgForIFM.encode())

            # send to EDM
            #msgForEDM = edm()
            #msgForEDM.time = currTime
            #msgForEDM.temp = currTemp
            #msgForEDM.flux = currFlux
            #lc.publish("EDM_CHAN", msgForEDM.encode())

            # send to NEW (py)

            # send to NEW (cpp)

        else:
            print("Waiting for messages...")
except KeyboardInterrupt:
    pass

# assume some calculations take 3 seconds
#print("\nsleep for 3 seconds... then kill proc")
#time.sleep(3)

# kill the sensor program if kill command given by user in main menu
x = sensorProc.kill()
print("**TRIED TO KILL the sensor subprocess! (but cannot confirm it)")

y = ifmProc.kill()
print("**TRIED TO KILL the IFM subprocess")

print("this is the end of main.py")
