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
  print(" --> MAIN RTFM recv %.4f from sensor #%d at %s" % (msg.sendTime, sid, timeStamp))

  # note: we are filling the globally scope newSensorData struct here
  newSensorData.sensorID = msg.sensorID
  newSensorData.sendTime = msg.sendTime


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

# launch event detection model (EDM)
userMsg1 = 'Ready to launch Event Detection Model? (Enter 0 or 1) '
start = raw_input(userMsg1)
if (start == "1"):
  edmProcess = subprocess.Popen(execEventDetection, shell=True)
else:
  print("***Event Detection Model was not started***")

# launch sensor simulator
userMsg2 = 'Ready to launch the Sensor Simulator? (Enter 0 or 1) '
start = raw_input(userMsg2)
if (start == "1"):
  sensorProcess = subprocess.Popen(execSensor, shell=True)
else:
  print("***Sensor Simulator was not started***")


# main event handling loop to:
#   1. recv new data from sensors
#   2. decide what to do with the data
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


# end of the main script
print("\n[END MAIN RTFM]\n")