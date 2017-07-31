#include <iostream>
#include <math.h>
#include "Sensor.h"

Sensor::Sensor()
{
  int i;
  for (i = 0; i < NUM_DATA; i++)
  {
    sensorData[i] = 0.0;
  }

  // define mapping from sensorData to physical values
  itime = 0;
  itemp = 1;
  iflux = 6;

  lastTime = 0.0;
  sumFEDheat1 = 0.0;
  sumFEDheat2 = 0.0;

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
  int warning = 0;

  // time and dt update
  double time = sensorData[itime];
  double dt = (time - lastTime) / 60.0;  // converted [sec] to [min]

  // convection 
  double temp = sensorData[itemp];
  double tc1, tc2, FED_c1, FED_c2;
  double A1, B1, A2, B2;
  A1 = 2.0 * pow(10.0, 31);
  B1 = 4.0 * pow(10.0, 8);
  A2 = 2.0 * pow(10.0, 18);
  B2 = 1.0 * pow(10.0, 8);
  tc1 = A1 * pow(temp, -16.963) + B1 * pow(temp, -3.7561);
  tc2 = A2 * pow(temp, -9.0403) + B2 * pow(temp, -3.10898);
  FED_c1 = dt / tc1;
  FED_c2 = dt / tc2;

  // radiation
  double flux = sensorData[iflux];
  double tr1, tr2, FED_r1, FED_r2;
  double r1, r2;
  double minFlux = 2.5;
  r1 = 1.33;
  r2 = 12.67;
  if (flux < minFlux)
  {
    tr1 = 30.0;
    tr2 = 30.0;
    FED_r1 = 0.0;
    FED_r2 = 0.0;
  }
  else
  {
    tr1 = r1 / pow(flux, 1.33);
    tr2 = tr1 * (r2 / r1);
    FED_r1 = dt / tr1;
    FED_r2 = dt / tr2;
  }

  // summation of FED and update time
  sumFEDheat1 += (FED_c1 + FED_r1);
  sumFEDheat2 += (FED_c2 + FED_r2);
  lastTime = time;

  if (sumFEDheat1 >= 1.0)
  {
    warning += 1;
  }
  if (sumFEDheat2 >= 1.0)
  {
    warning += 1;
  }

  return warning;
}

int Sensor::checkFireSpread()
{
  return 1;
}