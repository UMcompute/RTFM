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
  iO2 = 2;
  iCO = 3;
  iCO2 = 4;
  iHCN = 5;
  iflux = 6;

  lastTime = 0.0;
  sumFEDheat1 = 0.0;
  sumFEDheat2 = 0.0;
  sumFEDsmoke = 0.0;

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


void Sensor::updateTime()
{
  lastTime = sensorData[itime];
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

  /* *** CHECK UNITS OF ALL DATA USED IN THIS FUNCTION! ***

    CO [ppm]
    HCN [ppm]
    CO2 [%]
    O2 [%]

    For example, in the case of [%], use the "number":

    (20.9 - [O2])
    if [O2] = 6.5%, then use "6.5" in the equation:
    (20.9 - 6.5)

  */

  int warning = 0;
  double FED_CO, FED_CN, FED_NOx, FLD_irr, HV_CO2, FED_O2;
  double O2_limit = 7.0; // [%]

  // update time step
  double dt = (sensorData[itime] - lastTime) / 60.0;  // converted [sec] to [min]

  FED_CO = 2.764 * pow(10.0, -5) * pow(sensorData[iCO], 1.036) * dt;

  double NO2, NO, CN;
  NO2 = 0.0;
  NO = 0.0;
  CN = sensorData[iHCN] - NO2 - NO;
  FED_CN = ((1.0 / 220.0) * exp(CN / 43.0) - 0.0045) * dt;

  FED_NOx = 0.0;
  FLD_irr = 0.0;

  double x;
  double O2 = sensorData[iO2];  // [%]
  x = 8.13 - 0.54*(20.9 - O2);
  FED_O2 = dt / exp(x);

  double CO2 = sensorData[iCO2];  // [%]
  HV_CO2 = (1.0 / 7.1) * exp(0.1903 * CO2 + 2.0004);

  x = (FED_CO + FED_CN + FED_NOx + FLD_irr) * HV_CO2 + FED_O2;
  sumFEDsmoke += x;

  if (sumFEDsmoke >= 1.0)
  {
    warning += 1;
  }
  if (O2 < O2_limit)
  {
    warning += 1;
  }

  return warning;
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
  // THRESHOLD AND RATES-OF-INCREASE
  double maxTemp = 57.0;            // [C]
  double maxTempRate = 7.0;         // [C/min]
  double maxCO = 25.0;              // [ppm]  ==> (10-40), 50, and 25 suggested ***
  double maxCO2percent = 1.5;       // [%]
  double minO2percent = 17.0;       // [%]
  double maxRatioCOtoCO2 = 0.01;    // [unitless]

  int warning = 0;
  double tempRate = 0.0;

  // check temperature
  if (sensorData[itemp] > maxTemp)
  {
    warning += 1;
  }

  // compute the temperature rate using member function
  //tempRate = getTempRate();
  if (tempRate > maxTempRate)
  {
    warning += 1;
  }

  // check carbon monoxide
  if (sensorData[iCO] > maxCO)
  {
    warning += 1;
  }

  // check carbon dioxide
  if (sensorData[iCO2] > maxCO2percent)
  {
    warning += 1;
  }

  // check oxygen depletion
  if (sensorData[iO2] < minO2percent)
  {
    warning += 1;
  }

  // check ratio of CO to CO2
  // get CO2 as ppm first
  // ==>  conversion: 1ppm = 0.0001% gas
  double CO2ppm = sensorData[iCO2] * pow(10.0, 4);
  double gasRatio = 0.0;
  if (CO2ppm > 0.0)
  {
    gasRatio = sensorData[iCO] / CO2ppm;
    if (gasRatio > maxRatioCOtoCO2)
    {
      warning += 1;
    }
  }

  return warning;
}