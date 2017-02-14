# used for LCM to establish listener
import select
import time
import lcm
from toAAA import aaa


def my_handler(channel, data):
  msg = aaa.decode(data)
  #print("~~~~AAA Received message on channel \"%s\"" % channel)
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


print("starting AAA main...")

# initialize the LCM library
lc = lcm.LCM()
lc.subscribe("AAA_CHAN", my_handler)

currTime = 0.0
currTemp = 0.0
currFlux = 0.0

compTime = 2.5

# get sensor data using select function and waiting
try:
  timeout = 1.0  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      time.sleep(compTime)
    else:
      print("Waiting for messages in AAA main loop...")
except KeyboardInterrupt:
  pass

print("*todo: change the KeyboardInterrupt exit method for the AAA")

print("exit AAA main")
