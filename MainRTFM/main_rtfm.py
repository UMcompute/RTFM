# packages to include
import lcm
import select
import time

# LCM data structures
from sim_sensor import sensor_data

# LCM send data to sub-models
from send_to_ifm import data_to_ifm
from send_to_edm import data_to_edm

# LCM receive data from sub-models
from sent_by_ifm import data_from_ifm
from sent_by_edm import data_from_edm


# global variable for the number of rooms
global NUM_ROOMS
NUM_ROOMS = 4


ifm_time_step = 10.0
edm_time_step = 2.0


# handle new sensor data by assigning it to each Sensor class object
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
  sensorList[room].set_value(5, msg.HCNconc)
  sensorList[room].set_value(6, msg.heatFlux)

  # check if IFM data is ready to send based on IFM time step
  ifm_manager.check_time(sensorList[room].get_value(0), NUM_ROOMS)

  # check if EDM data is ready to send based on EDM time step
  edm_manager.check_time(sensorList[room].get_value(0), NUM_ROOMS)


# model_handler is currently only for the IFM
def model_handler(channel, data):
  msg = data_from_ifm.decode(data)
  print(channel)
  print(msg.current_HRR)


# currently assuming one sensor per room
# future: room can have zero, one, or multiple sensors in it 
class Sensor:
  NUM_DATA = 7

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
    # TODO: update this time checking scheme 
    #   (EDM missed one and failed to send from then on)
    if ((self.t1 < currTime) and (currTime < self.t2)):
      self.count += 1
    if ((self.count == numRooms) or (currTime > self.t2)):
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
ifm_manager = TimeManager(ifm_time_step)
ifm_data = data_to_ifm()
ifm_data.num_rooms = NUM_ROOMS
for i in range(0, NUM_ROOMS):
  ifm_data.temperature.append(0.0)
  ifm_data.oxygen_conc.append(0.0)
lc.subscribe("IFM_OUT_CHANNEL", model_handler)


# initialize the EDM time step manager
edm_manager = TimeManager(edm_time_step)
edm_data = data_to_edm()
edm_data.num_rooms = NUM_ROOMS
for i in range(0, NUM_ROOMS):
  edm_data.temperature.append(0.0)
  edm_data.O2_conc.append(0.0)
  edm_data.CO_conc.append(0.0)
  edm_data.CO2_conc.append(0.0)
  edm_data.HCN_conc.append(0.0)
  edm_data.heat_flux.append(0.0)

# MAIN LOOP
msg_time = []
start_time = time.time()
msg_time.append(start_time)
try:
  timeout = 0.01  # amount of time to wait, in seconds
  while True:
    rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
    if rfds:
      lc.handle()
      time_diff = time.time() - start_time
      msg_time.append(time_diff)
      # =======================================================================
      if (ifm_manager.sendFlag == 1):
        print("READY TO SEND DATA TO IFM")
        ifm_data.time_stamp = ifm_manager.sim_time - ifm_manager.sim_dt
        for i in range(0, NUM_ROOMS):
          # index 1 is the temperature in the Sensor class object
          ifm_data.temperature[i] = sensorList[i].get_value(1)
          # index 2 is the oxygen concentration in the Sensor class object
          ifm_data.oxygen_conc[i] = sensorList[i].get_value(2)
        # send complete message to IFM main loop
        lc.publish("IFM_CHANNEL", ifm_data.encode())
      # =======================================================================
      if (edm_manager.sendFlag == 1):
        print("READY TO SEND DATA TO EDM")
        edm_data.time_stamp = edm_manager.sim_time - edm_manager.sim_dt
        for i in range(0, NUM_ROOMS):
          # index 1 is the temperature in the Sensor class object
          edm_data.temperature[i] = sensorList[i].get_value(1)
          # index 2 is the oxygen concentration in the Sensor class object
          edm_data.O2_conc[i] = sensorList[i].get_value(2)
          # get the rest of the data values for the current package
          edm_data.CO_conc[i] = sensorList[i].get_value(3)
          edm_data.CO2_conc[i] = sensorList[i].get_value(4)
          edm_data.HCN_conc[i] = sensorList[i].get_value(5)
          edm_data.heat_flux[i] = sensorList[i].get_value(6)
        # send complete message to EDM main loop
        lc.publish("EDM_CHANNEL", edm_data.encode())
      # =======================================================================
    else:
      loopStatus = 1
except KeyboardInterrupt:
  pass
