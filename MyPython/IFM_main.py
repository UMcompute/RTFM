import select
import time
import lcm
from toIFM import ifm
from frIFM import ifmOUT


def my_handler(channel, data):
  msg = ifm.decode(data)
  #print("~~~~IFM Received message on channel \"%s\"" % channel)
  print("   IFM Current Time = %s" % str(msg.time))
  #print("   temp = %s" % str(msg.temp))
  #print("   flux = %s" % str(msg.flux))
  #print("\n")
  global currTime
  global currTemp
  global currFlux
  currTime = msg.time
  currTemp = msg.temp
  currFlux = msg.flux


print("starting IFM main...")

# initialize the LCM library
lc = lcm.LCM()
lc.subscribe("IFM_CHAN", my_handler)

currTime = 0.0
currTemp = 0.0
currFlux = 0.0

compTime = 5.0

# get sensor data using select function and waiting
try:
  timeout = 1.0  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      print("~~~ calculating value in IFM~~~")
      time.sleep(compTime)
      returnVal = ifmOUT()
      returnVal.currHRR = currTime ** 2
      print("~~~ done calculating in IFM ~~~")
      lc.publish("OUT_IFM", returnVal.encode())
    else:
      print("\n   [waiting for msg in IFM main loop]")
except KeyboardInterrupt:
  pass

print("*todo: change the KeyboardInterrupt exit method for the IFM")

print("exit IFM main")
