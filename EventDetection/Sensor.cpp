#include <iostream>
#include <math.h>
#include <stdio.h>
#include "Sensor.h"


Sensor::Sensor()
{
  // initialize sensor data with zeros
  int i;
  for (i = 0; i < NUM_DATA; i++)
  {
    sensorData[i] = 0.0;
  }

  // define mapping from sensorData array to physical values
  itime   = 0;
  itemp   = 1;
  iO2     = 2;
  iCO     = 3;
  iCO2    = 4;
  iHCN    = 5;
  iflux   = 6;

  // initial values of computed hazards
  lastTime = 0.0;
  lastTemp = 20.0;
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
  lastTemp = sensorData[itemp];
}


double Sensor::getFEDvals(int id)
{
  if (id == 0)
  {
    return sumFEDsmoke;
  }
  else if (id == 1)
  {
    return sumFEDheat1;
  }
  else if (id == 2)
  {
    return sumFEDheat2;
  }
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
  if (sensorData[itemp] >= maxTemp)
  {
    warning += 1;
  }
  if (sensorData[iflux] >= maxFlux)
  {
    warning += 1;
  }
  //printf("  flashover warning = %d \n", warning);
  return warning;
}


// Tested 08-10-17 at 11:45 with SFPE Handbook Table 63.22
int Sensor::checkSmokeTox()
{
  /* *** CHECK UNITS OF ALL DATA USED IN THIS FUNCTION! ***
    O2 [%]
    CO [ppm]
    CO2 [%]
    HCN [ppm]

    For example, in the case of [%], use the "number":
      if equation contains something like this: (20.9 - [O2])
      then say [O2] = 16.5%, 
      then use "16.5" directly in the equation: (20.9 - 16.5)
  */
  int warning = 0;
  int use_fds = 0;
  double FED_CO, FED_CN, FED_NOx, FLD_irr, HV_CO2, FED_O2;
  double O2_limit = 7.0; // [%] (Alarie 2002)
  double FED_limit = 1.0;

  // update time step
  double dt = (sensorData[itime] - lastTime) / 60.0;  // converted [sec] to [min]

  // FED for carbon monoxide
  FED_CO = 2.764 * pow(10.0, -5) * pow(sensorData[iCO], 1.036) * dt;

  // FED for CN which removes [NO2] and [NO] first
  // **note: we are not currently measuring [NO2] or [NO]
  double NO2, NO, CN;
  NO2 = 0.0;
  NO = 0.0;
  CN = sensorData[iHCN] - NO2 - NO;

  // use either the FDS or SFPE equation for [CN] exposure-dose
  if (use_fds == 1)
  {
    // FDS Eq. 17.20
    FED_CN = ((1.0 / 220.0) * exp(CN / 43.0) - 0.0045) * dt;
  }
  else
  {
    // SFPE Eq. 63.24
    FED_CN = ( pow(CN, 2.36) / 1200000.0 ) * dt;
  }

  // FED for any [NOx] present
  // **note: currently not measuring any [NOx]
  FED_NOx = 0.0;

  // FLD for irritants (none currently)
  // future: include HCl, HBr, formaldehyde, acrolein, HF, etc.
  FLD_irr = 0.0;

  // FED for O2 depletion
  double O2 = sensorData[iO2];  // [%]
  FED_O2 = dt / exp( 8.13 - 0.54*(20.9 - O2) );

  // Hyperventilation Factor
  if (use_fds == 1)
  {
    // FDS
    HV_CO2 = (1.0 / 7.1) * exp(0.1903 * sensorData[iCO2] + 2.0004);
  }
  else
  {
    // SFPE
    HV_CO2 = exp(sensorData[iCO2] / 5.0);
  }

  // update the smoke toxicity FED sum 
  sumFEDsmoke += ((FED_CO + FED_CN + FED_NOx + FLD_irr) * HV_CO2 + FED_O2);

  // check for 1.0 FED threshold and/or severe oxygen depletion
  if (sumFEDsmoke >= FED_limit)
  {
    warning += 1;
  }
  if (O2 <= O2_limit)
  {
    warning += 1;
  }
  /*
  // print output for unit test
  printf("  FED_CO = %6.2f\n", FED_CO);
  printf("  FED_CN = %6.2f\n", FED_CN);
  printf("  FED_O2 = %6.2f\n", FED_O2);
  printf("  HV_CO2 = %6.2f\n", HV_CO2);
  printf("  FEDtot = %6.2f\n", sumFEDsmoke);
  */
  return warning;
}


// Tested 08-10-17 at 09:00 with SFPE Handbook Table 63.22
int Sensor::checkBurnThreat()
{
  // warning initialization
  int warning = 0;
  double FED_limit = 1.0;

  // dt update
  double dt = (sensorData[itime] - lastTime) / 60.0;  // converted [sec] to [min]

  // convection contribution
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

  // radiation contribution
  double flux = sensorData[iflux];
  double tr1, tr2, FED_r1, FED_r2;
  double r1, r2;
  double minFlux = 2.5;
  r1 = 1.33;
  r2 = 16.7;
  if (flux < minFlux)
  {
    tr1 = 0.0;
    tr2 = 0.0;
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

  // summation of FED
  sumFEDheat1 += (FED_c1 + FED_r1);
  sumFEDheat2 += (FED_c2 + FED_r2);

  // warning check
  if (sumFEDheat1 >= FED_limit)
  {
    warning += 1;
  }
  if (sumFEDheat2 >= FED_limit)
  {
    warning += 1;
  }
  /*
  // print output for unit test
  printf("FED for pain: \n");
  printf("  convection = %8.2f\n", FED_c1);
  printf("  raditation = %8.2f\n", FED_r1);
  printf("  FEDpain(t) = %8.2f\n", FED_c1 + FED_r1);
  printf("  FEDsum(t)  = %8.2f\n", sumFEDheat1);
  printf("FED for full-thickness burns: \n");
  printf("  convection = %8.2f\n", FED_c2);
  printf("  raditation = %8.2f\n", FED_r2); 
  printf("  FEDfull(t) = %8.2f\n", FED_c2 + FED_r2);
  printf("  FEDsum(t)  = %8.2f\n", sumFEDheat2);
  */
  return warning;
}


// Tested 08-10-17 at 16:20 with SFPE Handbook Table 63.22
int Sensor::checkFireSpread()
{
  int method = 2;

  // THRESHOLDS AND RATES-OF-INCREASE
  double maxTemp = 57.0;            // [C]
  double maxTempRate = 7.0;         // [C/min]
  double maxCO = 40.0;              // [ppm]  ==> (10-40), 50, and 25 suggested ***
  double maxCO2percent = 1.5;       // [%]
  double minO2percent = 17.0;       // [%]
  double maxRatioCOtoCO2 = 0.01;    // [unitless]

  int warning = 0;
  double tempRate = 0.0;

  // dt update
  double dt = (sensorData[itime] - lastTime) / 60.0;  // converted [sec] to [min]

  // OPTION 1: ORIGINAL APPROACH
  if (method == 1)
  {
    // check temperature
    if (sensorData[itemp] >= maxTemp)
    {
      warning += 1;
    }

    // compute the temperature rate using member function
    tempRate = (sensorData[itemp] - lastTemp) / dt;
    if (tempRate >= maxTempRate)
    {
      warning += 1;
    }

    // check carbon monoxide
    if (sensorData[iCO] >= maxCO)
    {
      warning += 1;
    }

    // check carbon dioxide
    if (sensorData[iCO2] >= maxCO2percent)
    {
      warning += 1;
    }

    // check oxygen depletion
    if (sensorData[iO2] <= minO2percent)
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
      if (gasRatio >= maxRatioCOtoCO2)
      {
        warning += 1;
      }
    }
  }

  // OPTION 2: COMBINE RELATED CRITERIA
  if (method == 2)
  {
    // check temperature and temperature rate of increase
    tempRate = (sensorData[itemp] - lastTemp) / dt;
    //if (sensorData[itemp] >= maxTemp && tempRate >= maxTempRate)
    if (sensorData[itemp] >= maxTemp || tempRate >= maxTempRate)
    {
      warning += 1;
    }

    // check carbon monoxide, carbon dioxide, and ratio of them
    // get CO2 as ppm first
    // ==>  conversion: 1ppm = 0.0001% gas
    double CO2ppm = sensorData[iCO2] * pow(10.0, 4);
    double gasRatio = 0.0;
    if (CO2ppm > 0.0)
    {
      gasRatio = sensorData[iCO] / CO2ppm;
    }
    //if (sensorData[iCO] >= maxCO && sensorData[iCO2] >= maxCO2percent && gasRatio >= maxRatioCOtoCO2)
    if (sensorData[iCO] >= maxCO || gasRatio >= maxRatioCOtoCO2)
    {
      warning += 1;
    }

    // check oxygen depletion
    if (sensorData[iO2] <= minO2percent || sensorData[iCO2] >= maxCO2percent)
    {
      warning += 1;
    }
  }

  // impose a limit of 2 on the return
  warning = std::min(warning, 2);
  return warning;
}