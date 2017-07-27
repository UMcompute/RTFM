#include <iostream>
#include "Sensor.h"

Sensor::Sensor()
{
  int i;
  for (i = 0; i < NUM_DATA; i++)
  {
    sensorData[i] = 0.0;
  }

  // define mapping from sensorData to physical values
  itemp = 1;
  iflux = 6;

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

int Sensor::checkFlashover()
{
  // definitions of warning:
  //    if 0, no flashover
  //    if 1, possibly near flashover
  //    if 2, flashover conditions
  int warning = 0;
  double maxTemp = 600.0;
  double maxFlux = 20.0;
  if (sensorData[itemp] > maxTemp)
  {
    warning += 1;
  }
  if (sensorData[iflux] > maxFlux)
  {
    warning += 1;
  }
  return warning;
}

int Sensor::checkSmokeTox()
{
  return 1;
}

int Sensor::checkBurnThreat()
{
  return 1;
}

int Sensor::checkFireSpread()
{
  return 1;
}