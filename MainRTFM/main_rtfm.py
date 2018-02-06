# Python packages
import subprocess
import time

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
fr.close()
execEventDetection = "exec ../EventDetection/MainEDM.ex " + inputFile
execSensor = "exec ../Sensors/SimSensors.ex " + inputFile
# =========================================================


# fixed parameters
channelPrefix = "SENSOR"
timeout = 0.01          # amount of time to wait, in [sec]
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
userMsg1 = 'Ready to launch Event Detection Model? (Enter 0 or 1) '
startEDM = raw_input(userMsg1)
userMsg2 = 'Ready to launch the Sensor Simulator? (Enter 0 or 1) '
startSENS = raw_input(userMsg2)

# launch event detection model (EDM)
if (startEDM == "1"):
  edmProcess = subprocess.Popen(execEventDetection, shell=True)
  time.sleep(smallDelay)
else:
  print("***Event Detection Model was not started***")

# launch sensor simulator
if (startSENS == "1"):
  sensorProcess = subprocess.Popen(execSensor, shell=True)
  time.sleep(smallDelay)
else:
  print("***Sensor Simulator was not started***")


# ---------------------------------------------------------
# main event handling loop to do the following:
#   1. receive new data from any sensor
#   2. forward that data to sub-models (e.g. EDM)
newSensorData = sensor_data()
checkPoll = None
while (checkPoll == None):

  # check if the sensors are still active
  if 'sensorProcess' in locals():
    checkPoll = sensorProcess.poll()
  else:
    checkPoll = False

  # try to receive new data from a sensor
  rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
  if rfds:
    # a message was received from a sensor, get the new data
    lc.handle()

    # send the new data to EDM if it is active
    if 'edmProcess' in locals():
      lc.publish("EDM_CHANNEL", newSensorData.encode())

    # print brief update to terminal
    if (newSensorData.sensorID == 0):
      print( "  time = %.3f sec" % newSensorData.sendTime )

    # increment the data message counter
    sid = newSensorData.sensorID
    numMsgRecvPerSensor[sid] += 1
# ---------------------------------------------------------


# try to close event detection model if it is still running
maxTime = newSensorData.sendTime
if 'edmProcess' in locals():
  newSensorData.sendTime = killEDMtime
  lc.publish("EDM_CHANNEL", newSensorData.encode())
  time.sleep(smallDelay)
  checkPoll = edmProcess.poll()
  if (checkPoll == None):
    print("(***warning: EDM is still running***")
    # you can kill it with this Python command: edmProcess.kill()

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
print("\n[END MAIN RTFM]\n")
