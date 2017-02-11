# used for LCM to establish listener
import select
import time
import lcm
from toIFM import ifm


def my_handler(channel, data):
  msg = ifm.decode(data)
  print("~~~~IFM Received message on channel \"%s\"" % channel)
  print("    time = %s" % str(msg.time))
  #print("   temp = %s" % str(msg.temp))
  #print("   flux = %s" % str(msg.flux))
  print("\n")
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

# get sensor data using select function and waiting
try:
  timeout = 0.5  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      time.sleep(4)
    else:
      print("Waiting for messages in IFM main loop...")
except KeyboardInterrupt:
  pass

print("exit IFM main")
