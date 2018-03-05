# Python packages
import subprocess
import time
import sys

# LCM-related packages
import lcm
import select
from sensor import sensor_data


# handle new data coming from sensors
def sensor_handler(channel, data):
  timeStamp = time.strftime("%c")
  msg = sensor_data.decode(data)
  sid = msg.sensorID
  #print("\n --> MAIN RTFM recv %.3f from sensor #%d at %s" % (msg.sendTime, sid, timeStamp))

  # note: we are filling the globally scope newSensorData struct here
  newSensorData.sensorID = sid
  newSensorData.sendTime = msg.sendTime
  newSensorData.status = msg.status

  # (we are assuming that dim=3 and ndata=6)
  m = msg.dim
  n = msg.ndata
  newSensorData.dim = m
  newSensorData.ndata = n
  newSensorData.position[0:m] = msg.position[0:m] 
  newSensorData.data[0:n] = msg.data[0:n] 


# INPUT ===================================================
inputFile = "../Exec/input.txt"
fr = open(inputFile, 'r')
NUM_SENSORS = int( fr.readline() )
MAX_TIME = float( fr.readline() )
fr.close()
execEventDetection = "exec ../EventDetection/EDM.ex " + inputFile
execSensor = "exec ../Sensors/SensorSim.ex " + inputFile
execGenXML = "exec python ../Visualization/gen_xml_sched.py " + inputFile

# check for command line arguments to do automatic testing
numProcesses = 4
numArgs = len(sys.argv)
if ( numArgs == numProcesses ):
  startEDM = sys.argv[1]
  startSENS = sys.argv[2]
  startXML = sys.argv[3]
# =========================================================


# fixed parameters
channelPrefix = "SENSOR"
channelEDM = "EDM_CHANNEL"
timeout = 0.0001        # amount of time to wait, in [sec]
smallDelay = 1.0        # [sec]
killEDMtime = 100000.0  # [sec]

# initialize the LCM library
print("\n[START MAIN RTFM]\n")
lc = lcm.LCM()

# subscribe to all the sensor channels to recv new data
numMsgRecvPerSensor = []
for i in range(0, NUM_SENSORS):
  channel = channelPrefix + str(i)
  lc.subscribe(channel, sensor_handler)
  numMsgRecvPerSensor.append(0)

# prompt user to start sub-models
if ( numArgs != numProcesses ):
  userMsg1 = 'Ready to launch Event Detection Model? (Enter 0 or 1) '
  startEDM = raw_input(userMsg1)
  userMsg2 = 'Ready to launch the Sensor Simulator? (0 or 1) '
  startSENS = raw_input(userMsg2)
  if (startEDM == "1"):
    userMsg3 = 'Do you want to convert EDM output to XML? (0 or 1) '
    startXML = raw_input(userMsg3)

# launch event detection model (EDM)
if (startEDM == "1"):
  edmProcess = subprocess.Popen(execEventDetection, shell=True)
  time.sleep(smallDelay)
else:
  print("***Event Detection Model was not started***")

# launch sensor simulator
if (startSENS == "1"):
  sensorProcess = subprocess.Popen(execSensor, shell=True)
else:
  print("***Sensor Simulator was not started***")


# ---------------------------------------------------------
# main event handling loop to do the following:
#   1. receive new data from any sensor
#   2. forward that data to sub-models (e.g. EDM)
newSensorData = sensor_data()
checkPoll = None
currTime = 0.0
numComplete = 0
# while ( checkPoll == None or numComplete < NUM_SENSORS ):
while ( checkPoll == None or (currTime < MAX_TIME and numComplete < NUM_SENSORS) ):

  # check if the sensors are still active
  if 'sensorProcess' in locals():
    checkPoll = sensorProcess.poll()
  else:
    checkPoll = False
    numComplete = NUM_SENSORS

  # try to receive new data from a sensor
  rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
  if rfds:
    # a message was received from a sensor, get the new data
    lc.handle()
    checkPoll = None

    # send the new data to EDM if it is active
    if 'edmProcess' in locals():
      lc.publish(channelEDM, newSensorData.encode())

    # print a brief update to terminal
    currTime = newSensorData.sendTime
    if (newSensorData.sensorID == 0):
      print( "  time = %.3f sec" % currTime )

    # increment the data message counter
    sid = newSensorData.sensorID
    numMsgRecvPerSensor[sid] += 1
    if (currTime >= MAX_TIME):
      numComplete += 1
# ---------------------------------------------------------


# try to close event detection model if it is still running
maxTime = newSensorData.sendTime
if 'edmProcess' in locals():
  newSensorData.sendTime = killEDMtime
  lc.publish(channelEDM, newSensorData.encode())
  time.sleep(smallDelay)
  checkPoll = edmProcess.poll()
  if (checkPoll == None):
    print("(***warning: EDM is still running***")

# write EDM output in XML format
if ('startXML' in locals() and startXML == "1"):
  XMLprocess = subprocess.Popen(execGenXML, shell=True)
  checkPoll = None
  while (checkPoll == None):
    checkPoll = XMLprocess.poll()
time.sleep(smallDelay)

# prepare some statistics about the data received from sensors
totalRecv = 0
sid = 0
minRecv = [ numMsgRecvPerSensor[sid], sid ]
maxRecv = [ numMsgRecvPerSensor[sid], sid ]
for count in numMsgRecvPerSensor:
  if (count < minRecv[0]):
    minRecv = [count, sid]
  if (count > maxRecv[0]):
    maxRecv = [count, sid]
  totalRecv += count
  sid += 1

# aggregate stats
avgRecv = float(totalRecv) / float(NUM_SENSORS)
if (maxTime > 0.0):
  msgPerSec = float(totalRecv) / maxTime
else:
  msgPerSec = 0.0

# end of the main script
print("\n\tMessages received from all %d sensors:" % NUM_SENSORS)
print("\t" + str(numMsgRecvPerSensor))
print("\n\t[MAIN RTFM SUMMARY]")
print("\t  %d total number of data messages received" % totalRecv)
print("\t  %d minimum messages sent from sensor #%d" % (minRecv[0], minRecv[1]) )
print("\t  %d maximum messages sent from sensor #%d" % (maxRecv[0], maxRecv[1]) )
print("\t  %.2f average messages sent from all sensors" %  avgRecv)
print("\t  %.2f average messages received per second" %  msgPerSec)
print("\t  %.3f total time in MAIN RTFM" %  maxTime)
print("\n[END MAIN RTFM]\n")

