# Python packages
import subprocess
import select
import time

# LCM packages
import lcm

# LCM data structures
from sensor import sensor_data

# global variables (move to input file?)
global NUM_SENSORS


# handle new data coming from sensors
def sensor_handler(channel, data):
  timeStamp = time.strftime("%c")
  msg = sensor_data.decode(data)
  sid = msg.sensorID
  print("\n --> MAIN RTFM recv %.3f from sensor #%d at %s" % (msg.sendTime, sid, timeStamp))

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


print("\n[START MAIN RTFM]\n")
# INPUT ===================================================
NUM_SENSORS = 4
timeout = 0.01  # amount of time to wait, in seconds
channelPrefix = "SENSOR"
execEventDetection = "exec ../EventDetection/MainEDM.ex"
execSensor = "exec ../Sensors/SimSensors.ex"
# =========================================================

# initialize the LCM library
lc = lcm.LCM()

# subscribe to all the sensor channels to recv new data
for i in range(0, NUM_SENSORS):
  channel = channelPrefix + str(i)
  lc.subscribe(channel, sensor_handler)

# prompt user to start sub-models
userMsg1 = 'Ready to launch Event Detection Model? (Enter 0 or 1) '
startEDM = raw_input(userMsg1)
userMsg2 = 'Ready to launch the Sensor Simulator? (Enter 0 or 1) '
startSENS = raw_input(userMsg2)

# launch event detection model (EDM)
smallDelay = 0.5
if (startEDM == "1"):
  time.sleep(smallDelay)
  edmProcess = subprocess.Popen(execEventDetection, shell=True)
else:
  print("***Event Detection Model was not started***")

# launch sensor simulator
if (startSENS == "1"):
  time.sleep(smallDelay)
  sensorProcess = subprocess.Popen(execSensor, shell=True)
else:
  print("***Sensor Simulator was not started***")


# main event handling loop to do the following:
#   1. receive new data from any sensor
#   2. forward that data to sub-models (e.g. EDM)

newSensorData = sensor_data()
checkPoll = None
while (checkPoll == None):

  # check if the sensors are still active
  checkPoll = sensorProcess.poll()

  # try to receive new data from a sensor
  rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
  if rfds:
    # a message was received from a sensor, get the new data
    lc.handle()

    # send the new data to EDM if it is active
    lc.publish("EDM_CHANNEL", newSensorData.encode())

# try to close event detection model if it is still running
checkPoll = edmProcess.poll()
if (checkPoll == None):
  edmProcess.kill()

# end of the main script
print("\n[END MAIN RTFM]\n")