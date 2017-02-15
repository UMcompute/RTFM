import select
import time
import lcm
from toAAA import aaa
from frAAA import aaaOUT


def my_handler(channel, data):
  msg = aaa.decode(data)
  #print("~~~~AAA Received message on channel \"%s\"" % channel)
  print("   AAA Current Time = %s" % str(msg.time))
  #print("   temp = %s" % str(msg.temp))
  #print("   flux = %s" % str(msg.flux))
  #print("\n")
  global currTime
  global currTemp
  global currFlux
  currTime = msg.time
  currTemp = msg.temp
  currFlux = msg.flux


print("starting AAA main...")

# initialize the LCM library
lc = lcm.LCM()
lc.subscribe("AAA_CHAN", my_handler)

currTime = 0.0
currTemp = 0.0
currFlux = 0.0

compTime = 1.0
x = 1.0
# get sensor data using select function and waiting
try:
  timeout = 1.0  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds: 
      lc.handle()
      print("+++ calculating value in AAA+++")
      time.sleep(compTime)
      x = x + x
      returnVal = aaaOUT()
      returnVal.dumVal = x  
      print("+++ done calculating in AAA +++")
      lc.publish("OUT_AAA", returnVal.encode())
    else:
      print("\n   [waiting for msg in AAA main loop]")
except KeyboardInterrupt:
  pass

print("*todo: change the KeyboardInterrupt exit method for the AAA")

print("exit AAA main")
