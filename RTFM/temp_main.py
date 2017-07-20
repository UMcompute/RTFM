import lcm
import select

from sensor import sensor_data


# handle new data by assigning it to each Sensor class object
def msg_handler(channel, data):
  msg = sensor_data.decode(data)
  print("Received msg from room %d on channel \"%s\" at time %f" % (msg.roomNum, channel, msg.sendTime))
  # specifically assign new data values
  sensorList[msg.roomNum].set_value(0, msg.sendTime)
  sensorList[msg.roomNum].set_value(1, msg.temperature)
  sensorList[msg.roomNum].set_value(2, msg.O2conc)
  sensorList[msg.roomNum].set_value(3, msg.COconc)
  sensorList[msg.roomNum].set_value(4, msg.CO2conc)
  sensorList[msg.roomNum].set_value(5, msg.heatFlux)


# currently assuming one sensor per room
# future: room can have zero, one, or multiple sensors in it 
class Sensor:
  NUM_DATA = 6

  def __init__(self, myRoom):
    self.room_id = myRoom
    self.my_data = []
    for i in range(0, self.NUM_DATA):
      self.my_data.append(0.0)

  def set_value(self, index, newValue):
    self.my_data[index] = newValue

  def get_value(self, index):
    return self.my_data[index]

  def print_value(self, index):
    print("Room #%d has value %f at %d" % (self.room_id, self.my_data[index], index))


# initialize the LCM library
lc = lcm.LCM()

# subscribe to each room's channel and generate new sensor objects
NUM_ROOMS = 4
sensorList = []
for i in range(0, NUM_ROOMS):
  channel = "ROOM" + str(i)
  lc.subscribe(channel, msg_handler)
  sensorList.append(Sensor(i))

# MAIN LOOP
msg_count = 0
try:
  timeout = 0.1  # amount of time to wait, in seconds
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
