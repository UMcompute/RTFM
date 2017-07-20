# packages to include
import lcm
import select

# LCM data structures
from sensor import sensor_data

# global variable for the number of rooms
global NUM_ROOMS
NUM_ROOMS = 4


# handle new data by assigning it to each Sensor class object
def msg_handler(channel, data):
  msg = sensor_data.decode(data)
  room = msg.roomNum
  print("Received msg from room %d on channel \"%s\" at time %f" % (room, channel, msg.sendTime))
  
  # specifically assign new data values based on LCM struct
  sensorList[room].set_value(0, msg.sendTime)
  sensorList[room].set_value(1, msg.temperature)
  sensorList[room].set_value(2, msg.O2conc)
  sensorList[room].set_value(3, msg.COconc)
  sensorList[room].set_value(4, msg.CO2conc)
  sensorList[room].set_value(5, msg.heatFlux)

  # check if IFM data is ready to send based on IFM time step
  ifm_manager.check_time(sensorList[room].get_value(0), NUM_ROOMS)


# currently assuming one sensor per room
# future: room can have zero, one, or multiple sensors in it 
class Sensor:
  NUM_DATA = 6

  def __init__(self, myRoom):
    print("NEW ROOM CREATED WITH ONE SENSOR!")
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


# manager class to determine when to send message to sub-models
class TimeManager:
  tol = 0.5

  def __init__(self, dt):
    self.count = 0
    self.sim_dt = dt
    self.sim_time = dt
    self.t1 = dt - self.tol
    self.t2 = dt + self.tol
    self.sendFlag = 0

  def check_time(self, currTime, numRooms):
    if ((self.t1 < currTime) and (currTime < self.t2)):
      self.count += 1
    if (self.count == numRooms):
      # now we are ready to send data to sub-model
      self.sendFlag = 1
      self.sim_time += self.sim_dt
      self.t1 = self.sim_time - self.tol
      self.t2 = self.sim_time + self.tol
      self.count = 0
    else:
      self.sendFlag = 0


# initialize the LCM library
lc = lcm.LCM()

# subscribe to each room's channel and generate new sensor objects
sensorList = []
for i in range(0, NUM_ROOMS):
  channel = "ROOM" + str(i)
  lc.subscribe(channel, msg_handler)
  sensorList.append(Sensor(i))

# initialize the IFM time step manager
ifm_time_step = 5.0
ifm_manager = TimeManager(ifm_time_step)

# MAIN LOOP
try:
  timeout = 0.01  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      # =============================================================
      if (ifm_manager.sendFlag == 1):
        print("READY TO SEND DATA TO IFM")
      # =============================================================
    else:
      loopStatus = 1
except KeyboardInterrupt:
  pass
