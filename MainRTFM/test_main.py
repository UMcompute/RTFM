import time
import subprocess

# I want to launch a C++ program from this Python main program,
# but I don't want this Python code to wait for C++ program to finish. 

print("\n[START MAIN RTFM]\n")

# launch sensor simulator
execSensor = "exec ./QueueSensors.ex"
userMsg = 'Ready to launch the sensors? (Enter 0 or 1) '

startSensors = raw_input(userMsg)
if (startSensors == "1"):
  sensorProcess = subprocess.Popen(execSensor, shell=True)
else:
  print("***Sensor simulation was not started***")

# do my own work in main while the sensors run:
checkPoll = None
while (checkPoll == None):
  checkPoll = sensorProcess.poll()
  # doing work via sleep
  time.sleep(0.100)
  #print("-------------------")

print("\n[END MAIN RTFM]\n")