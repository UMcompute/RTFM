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
from frEDM import edmOUT


def my_handler(channel, data):
  msg = sensor.decode(data)
  #print("\nMAIN.py Received message on channel \"%s\"" % channel)
  #print("   time = %s" % str(msg.time))
  #print("   temp = %s" % str(msg.temp))
  #print("   flux = %s" % str(msg.flux))
  #print("\n")
  global currTime
  global currTemp
  global currFlux
  currTime = msg.time
  currTemp = msg.temp
  currFlux = msg.flux


def edm_handler(channel, data):
  msg = edmOUT.decode(data)
  print("\n  current temperature slope = " + str(msg.tempSlope))


# ===================================================================
# START THE MAIN PROGRAM LOOP

print("this is the start of main.py")

# initialize the LCM library
lc = lcm.LCM()
lc.subscribe("SENSOR", my_handler)

lc2 = lcm.LCM()
lc2.subscribe("EDM_OUT", edm_handler)


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
ifmDT = 5

# start subprocess for EDM
print("\n***warning for testing: make sure EDM_main.cpp has been compiled")
edmStart = './EDM_main.exe'
edmProc = subprocess.Popen("exec " + edmStart, shell=True)


# ===================================================================
# START RECEIVER TO GET SENSOR DATA INTO MAIN LOOP

# get sensor data using select function and waiting
numMsgRecv = 0
ifmStep = 1
try:
  timeout = 0.5  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      numMsgRecv = numMsgRecv + 1

# ===================================================================
      # distribute data to the running subprocess models

      # send to IFM
      if numMsgRecv == ifmStep:
        msgForIFM = ifm()
        msgForIFM.time = currTime
        msgForIFM.temp = currTemp
        msgForIFM.flux = currFlux
        lc.publish("IFM_CHAN", msgForIFM.encode())
        ifmStep = ifmStep + ifmDT

      # send to EDM
      msgForEDM = edm()
      msgForEDM.time = currTime
      msgForEDM.temp = currTemp
      msgForEDM.flux = currFlux
      lc.publish("EDM_CHAN", msgForEDM.encode())

      # send to NEW (py)

      # send to NEW (cpp)

# ===================================================================
      # get data from other modules
      #try:
      timeout2 = 0.2  # amount of time to wait, in seconds
      #while True:
      rfds2, wfds2, efds2 = select.select([lc2.fileno()], [], [], timeout2)
      if rfds2:
        lc2.handle()
      else:
        yy = 14.0
      #except KeyboardInterrupt:
      #pass
# ===================================================================
    else:
      zz = 12.0
      #print("Waiting for messages in MAIN program loop...")
except KeyboardInterrupt:
  pass

# assume some calculations take 3 seconds
#print("\nsleep for 3 seconds... then kill proc")
#time.sleep(3)

# kill the sensor program if kill command given by user in main menu
x = sensorProc.kill()
print("\n**TRIED TO KILL the sensor subprocess! (but cannot confirm it)")

y = ifmProc.kill()
print("\n**TRIED TO KILL the IFM subprocess! (but cannot confirm it)")

z = edmProc.kill()
print("\n**TRIED TO KILL the EDM subprocess! (but cannot confirm it)")

print("\nVisually inspect ps output here to see if subprocess is still running: ")
os.system("ps")

print("this is the end of main.py")
