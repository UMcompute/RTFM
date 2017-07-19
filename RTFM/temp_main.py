import lcm
import select

from sensor import sensor_data


def my_handler(channel, data):
  msg = sensor_data.decode(data)
  print("Received message on channel \"%s\" at time %f" % (channel, msg.sendTime))
  '''
  print("   timestamp   = %s" % str(msg.timestamp))
  print("   position    = %s" % str(msg.position))
  print("   orientation = %s" % str(msg.orientation))
  print("   ranges: %s" % str(msg.ranges))
  print("   name        = '%s'" % msg.name)
  print("   enabled     = %s" % str(msg.enabled))
  '''
  print("")


# initialize the LCM library
lc = lcm.LCM()

# subscribe to each room's channel
NUM_ROOMS = 4
for i in range(0, NUM_ROOMS):
  channel = "ROOM" + str(i)
  lc.subscribe(channel, my_handler)

# MAIN LOOP
msg_count = 0
try:
  timeout = 0.2  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      # =============================================================
      if (msg_count < NUM_ROOMS - 1):
        msg_count += 1
      else:
        print("ROUND OF DATA COMPLETE %d \n" % msg_count)
        msg_count = 0
      # =============================================================
    else:
      loopStatus = 1
except KeyboardInterrupt:
  pass