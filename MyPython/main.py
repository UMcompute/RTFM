# general packages to include
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

# used for communication with visualization devices
import urllib
import re


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
  global currSlope
  currSlope = msg.tempSlope
  print("   current temperature slope = " + str(currSlope))


def ifm_handler(channel, data):
  global pathFlag
  pathFlag = 2
  global busyIFM
  busyIFM = 0
  msg = ifmOUT.decode(data)
  global currHRR
  currHRR = msg.currHRR
  print("   current heat release rate = " + str(currHRR))


def aaa_handler(channel, data):
  global pathFlag
  pathFlag = 3
  global busyAAA
  busyAAA = 0
  msg = aaaOUT.decode(data)
  global currDummy
  currDummy = msg.dumVal
  print("   current dummy value = " + str(currDummy))


# ===================================================================
# START THE MAIN PROGRAM LOOP

print("this is the start of main.py")

TEST_WITH_VIZ_MODULE = 1
testing_input = 1

if TEST_WITH_VIZ_MODULE == 1:
  # initialize model start flags
  launchSENS = 0
  launchEDM = 0
  launchIFM = 0
  launchAAA = 0
else:
  # for testing only: turn OFF (0) or ON (1)
  launchSENS = 1
  launchEDM = 0
  launchIFM = 0
  launchAAA = 0

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WAIT FOR STARTING FLAG FROM VISUALIZATION CONTROL DEVICE
if TEST_WITH_VIZ_MODULE == 1:
  if testing_input == 1:
    IP_VIZ = raw_input('enter IP address of vizualization device: ')
    PORT_VIZ = raw_input('enter port # of vizualization device: ')
    # example: enter 141.213.169.232 for IP address
    # example: enter 8080 for port #
  else:
    IP_VIZ = "141.212.44.241"
    PORT_VIZ = "8080"
  FILENAME = "status.txt"
  check_timeout = 1.0
  check_count = 0
  check_limit = 1000

  # use urllib package to get file from server
  full_download_name = "http://" + IP_VIZ + ":" + PORT_VIZ + "/" + FILENAME
  full_save_name = "./" + FILENAME
  start_main = 0
  print("\nwaiting for signal from remote device to begin ...")
  while check_count < check_limit and start_main == 0:
    check_count = check_count + 1
    time.sleep(check_timeout)
    # check if the status file contains the start key
    retResult = urllib.urlretrieve(full_download_name, full_save_name)
    #print(retResult)
    file = open(full_save_name, "r")
    for line in file:
      if re.search("start", line):
        print("time to start main program")
        start_main = 1
      elif start_main == 1:
        input_list = line.split(',')
        print("user input these values for models: " + str(input_list))
        for inp in range(len(input_list)):
          modelFlag = int(input_list[inp])
          if modelFlag == 1:
            if inp == 0:
              launchSENS = 1
            elif inp == 1:
              launchEDM = 1
            elif inp == 2:
              launchIFM = 1
            elif inp == 3:
              launchAAA = 1
      #else:
      #  print line
      # elif start_main == 1:
      #   input_list = line.split(',')
      #   for inp in len(input_list):
      #     print("start subprocess #", str(inp)
    file.close()
  if check_count == check_limit:
    print("***warning: possible error due to timeout waiting for starting signal")
# NOW MAIN PROGRAM IS READY TO BEGIN
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# initialize the LCM library
lc = lcm.LCM()

# subscribe to any active channels from models
if launchSENS == 1:
  lc.subscribe("SENSOR", my_handler)
if launchEDM == 1:
  lc.subscribe("OUT_EDM", edm_handler)
if launchIFM == 1:  
  lc.subscribe("OUT_IFM", ifm_handler)
if launchAAA == 1:
  lc.subscribe("OUT_AAA", aaa_handler)

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

# ===================================================================
# LAUNCH SENSOR WITH FIRE DATA FILE

# launch main menu for user
# todo: include kill process option in menu for user to kill sensor
'''
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
'''

# start the single sensor for dev mode at beginning of Main program only
if launchSENS == 1:
  print("\n***warning for testing: ignoring main menu and using 1 pre-defined sensor")
  dataName = 'FDS_FirstMin.dat'
  sensorDir = './fromSensors/'
  sensorName = 'sensor.exe' + ' ' + sensorDir + dataName 
  fullExePath = sensorDir + sensorName
  time.sleep(2.0)  
  # this sleep step was used to ensure that the other subprocesses have started first
  # TODO: we can find a better "BARRIER" function for this purpose instead of sleep
  sensorProc = subprocess.Popen("exec " + fullExePath, shell=True)
  '''
  notStarted = 1
  while notStarted == 1:
    if launchEDM == 1:
      edmRet = edmProc.returncode
    else:
      edmRet = None
    if launchIFM == 1:
      ifmRet = ifmProc.returncode
    else:
      ifmRet = None
    if launchAAA == 1:
      aaaRet = aaaProc.returncode
    else:
      aaaRet = None
    if edmRet == None and ifmRet == None and aaaRet == None:
      sensorProc = subprocess.Popen("exec " + fullExePath, shell=True)
      notStarted = 0
    else:
      print("(waiting for all subprocesses to start)")
  '''

# ===================================================================
# START RECEIVERS TO GET SENSOR DATA AND MODEL UPDATES IN MAIN LOOP

# flags to differentiate proper work path
pathFlag = 0

# busy or ready status of each process
busyEDM = 0
busyIFM = 0
busyAAA = 0

# first version of output file
outFile = open('update.csv', 'w')
outFile.write('SENSOR, SENSOR, SENSOR, EDM, IFM, AAA\n')

# initialize output values
currTime = 0.0
currTemp = 0.0
currFlux = 0.0
currSlope = 0.0
currHRR = 0.0
currDummy = 0.0

# MAIN LOOP
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

        # write most recent data to output file
        outFile.write(str(currTime) + ', ' + str(currTemp) + ', ' + str(currFlux) + ', ')
        outFile.write(str(currSlope)+ ', ' + str(currHRR)  + ', ' + str(currDummy) + '\n')
# ===================================================================
      '''
      elif pathFlag == 1:
        print("   new msg from EDM")
      elif pathFlag == 2:
        print("   new msg from IFM")
      elif pathFlag == 3:
        print("   new msg from AAA")
      '''
    else:
      loopStatus = 1
      #print("\n   [waiting for new messages in MAIN program loop]")
except KeyboardInterrupt:
  pass

# kill the subprocess programs if still active waiting for work
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

# close the output file
outFile.close()

# end the main program and return to the terminal
#print("\nVisually inspect ps output here to see if subprocess is still running: ")
#os.system("ps")
print("\nthis is the end of main.py\n")
