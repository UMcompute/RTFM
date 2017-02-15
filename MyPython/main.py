import subprocess
import time
import os
import signal
from time import gmtime, strftime

# used for LCM to establish listener
import select
import lcm
from fromSensor import sensor
from frEDM import edmOUT
from frIFM import ifmOUT
from frAAA import aaaOUT

# used for LCM to establish sender
from toIFM import ifm
from toEDM import edm
from toAAA import aaa


def my_handler(channel, data):
  global pathFlag
  pathFlag = 0
  msg = sensor.decode(data)
  #print("   MAIN timestamp = " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
  #print("\nMAIN.py Received message on channel \"%s\"" % channel)
  print("   MAIN got time = %s" % str(msg.time))
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
  global pathFlag
  pathFlag = 1
  global busyEDM
  busyEDM = 0
  msg = edmOUT.decode(data)
  print("   current temperature slope = " + str(msg.tempSlope))


def ifm_handler(channel, data):
  global pathFlag
  pathFlag = 2
  global busyIFM
  busyIFM = 0
  msg = ifmOUT.decode(data)
  print("   current heat release rate = " + str(msg.currHRR))


def aaa_handler(channel, data):
  global pathFlag
  pathFlag = 3
  global busyAAA
  busyAAA = 0
  msg = aaaOUT.decode(data)
  print("   current dummy value = " + str(msg.dumVal))


# ===================================================================
# START THE MAIN PROGRAM LOOP

print("this is the start of main.py")

TEST_WITH_VIZ_MODULE = 0

if TEST_WITH_VIZ_MODULE == 1:
  # initialize model start flags
  launchSENS = 0
  launchEDM = 0
  launchIFM = 0
  launchAAA = 0
else:
  # for testing only: turn OFF (0) or ON (1)
  launchSENS = 1
  launchEDM = 1
  launchIFM = 1
  launchAAA = 1

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WAIT FOR STARTING FLAG FROM VISUALIZATION CONTROL DEVICE
if TEST_WITH_VIZ_MODULE == 1:
  IP_VIZ = raw_input('enter IP address of vizualization device: ')
  check_timeout = 1.0
  check_count = 0
  check_limit = 1000
  while check_count < check_limit:
    check_count = check_count + 1
    time.sleep(check_timeout)
    os.system("wget ")
# NOW MAIN PROGRAM IS READY TO BEGIN
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# initialize the LCM library
lc = lcm.LCM()

if launchSENS == 1:
  lc.subscribe("SENSOR", my_handler)
if launchEDM == 1:
  lc.subscribe("OUT_EDM", edm_handler)
if launchIFM == 1:  
  lc.subscribe("OUT_IFM", ifm_handler)
if launchAAA == 1:
  lc.subscribe("OUT_AAA", aaa_handler)

#lc2 = lcm.LCM()
#lc2.subscribe("EDM_OUT", edm_handler)

# start subprocess for EDM
if launchEDM == 1:
  print("\n***warning for testing: make sure EDM_main.cpp has been compiled")
  edmStart = './EDM_main.exe'
  edmProc = subprocess.Popen("exec " + edmStart, shell=True)

# start subprocess for IFM
if launchIFM == 1:
  ifmStart = 'python IFM_main.py'
  ifmProc = subprocess.Popen("exec " + ifmStart, shell=True)

# start subprocess for AAA
if launchAAA == 1:
  aaaStart = 'python AAA_main.py'
  aaaProc = subprocess.Popen("exec " + aaaStart, shell=True)

# time.sleep(1.0)

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
if launchSENS == 1:
  print("\n***warning for testing: ignoring main menu and using 1 pre-defined sensor")
  dataName = 'FDS_FirstMin.dat'
  sensorDir = './fromSensors/'
  sensorName = 'sensor.exe' + ' ' + sensorDir + dataName 
  fullExePath = sensorDir + sensorName
  sensorProc = subprocess.Popen("exec " + fullExePath, shell=True)

# ===================================================================
# START RECEIVER TO GET SENSOR DATA INTO MAIN LOOP

# flags to differentiate proper work path
pathFlag = 0

# busy or ready status of each process
busyEDM = 0
busyIFM = 0
busyAAA = 0

try:
  timeout = 0.2  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
# ===================================================================
      # distribute data to the ready ("not busy") subprocess models
      print("   pathFlag = " + str(pathFlag) + " and busy signals are " + str(busyEDM) + " " + str(busyIFM) + " " + str(busyAAA))
      # print busyIFM next!
      if pathFlag == 0:
        # send to EDM
        if launchEDM == 1 and busyEDM == 0:
          msgForEDM = edm()
          msgForEDM.time = currTime
          msgForEDM.temp = currTemp
          msgForEDM.flux = currFlux
          busyEDM = 1
          lc.publish("EDM_CHAN", msgForEDM.encode())
          print("***sent data to EDM ===>")
        # send to IFM 
        if launchIFM == 1 and busyIFM == 0:
          msgForIFM = ifm()
          msgForIFM.time = currTime
          msgForIFM.temp = currTemp
          msgForIFM.flux = currFlux
          busyIFM = 1
          lc.publish("IFM_CHAN", msgForIFM.encode())
          print("***sent data to IFM ===>")
        # send to NEW (py) --> named AAA for now
        if launchAAA == 1 and busyAAA == 0:
          msgForAAA = aaa()
          msgForAAA.time = currTime
          msgForAAA.temp = currTemp
          msgForAAA.flux = currFlux
          busyAAA = 1
          lc.publish("AAA_CHAN", msgForAAA.encode())
          print("***sent data to AAA ===>")

      # elif pathFlag == 1:
      #   print("   new msg from EDM")
      # elif pathFlag == 2:
      #   print("   new msg from IFM")
      # elif pathFlag == 3:
      #   print("   new msg from AAA")

# ===================================================================
    else:
      zzz = 12.0
      #print("Waiting for new data from sensors in MAIN program loop...")
except KeyboardInterrupt:
  pass

# assume some calculations take 3 seconds
#print("\nsleep for 3 seconds... then kill proc")
#time.sleep(3)

# kill the sensor program if kill command given by user in main menu
if launchSENS == 1:
  sensorProc.kill()
  print("\n**TRIED TO KILL the sensor subprocess! (but cannot confirm it)")

if launchEDM == 1:
  edmProc.kill()
  print("\n**TRIED TO KILL the EDM subprocess! (but cannot confirm it)")

if launchIFM == 1:
  ifmProc.kill()
  print("\n**TRIED TO KILL the IFM subprocess! (but cannot confirm it)")

if launchAAA == 1:
  aaaProc.kill()
  print("\n**TRIED TO KILL the AAA subprocess! (but cannot confirm it)")  

print("\nVisually inspect ps output here to see if subprocess is still running: ")
os.system("ps")

print("this is the end of main.py")
