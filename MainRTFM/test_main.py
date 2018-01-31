# Python packages
import subprocess
import select
import time

# LCM packages
import lcm

# LCM data structures
from sim_sensor import sensor_data

# global variables (move to input file?)
global NUM_SENSORS


# handle new data coming from sensors
def sensor_handler(channel, data):
  timeStamp = time.strftime("%c")
  msg = sensor_data.decode(data)
  sid = msg.sensorID
  print(" --> MAIN RTFM recv %.4f from sensor #%d at %s" % (msg.sendTime, sid, timeStamp))


print("\n[START MAIN RTFM]\n")
# INPUT ===================================================
NUM_SENSORS = 4
timeout = 0.01  # amount of time to wait, in seconds
channelPrefix = "SENSOR"
execSensor = "exec ../Sensors/QueueSensors.ex"
# =========================================================

# initialize the LCM library
lc = lcm.LCM()

# subscribe to all the sensor channels to recv new data
for i in range(0, NUM_SENSORS):
  channel = channelPrefix + str(i)
  lc.subscribe(channel, sensor_handler)

# launch sensor simulator
userMsg = 'Ready to launch the sensors? (Enter 0 or 1) '
startSensors = raw_input(userMsg)
if (startSensors == "1"):
  sensorProcess = subprocess.Popen(execSensor, shell=True)
else:
  print("***Sensor simulation was not started***")

# main event handling loop to:
#   1. recv new data from sensors
#   2. decide what to do with the data
checkPoll = None
while (checkPoll == None):
  checkPoll = sensorProcess.poll()
  rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
  if rfds:
    lc.handle()

# end of the main script
print("\n[END MAIN RTFM]\n")