#include <iostream>
#include "Sensor.h"

Sensor::Sensor()
{
  int i;
  for (i = 0; i < NUM_DATA; i++)
  {
    sensorData[i] = 0.0;
  }
  std::cout << "new sensor created" << std::endl;
}

Sensor::~Sensor()
{
  std::cout << "deleted a sensor" << std::endl;
}

void Sensor::setID(int myID)
{
  roomID = myID;
  std::cout << "my room id is " << roomID << std::endl;
}

void Sensor::setData(int index, double newData)
{
  sensorData[index] = newData;
}