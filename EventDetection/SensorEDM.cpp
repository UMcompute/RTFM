#include <stdio.h>
#include <fstream>
#include <math.h>

#include "SensorEDM.h"
#include "DataHandler.h"


SensorEDM::SensorEDM()
{
  // initialize the hazard variables:
  sumFEDsmoke = 0.0;
  fireStatus = 0;
  lastTime = 0.0;
  dt = 0.0;
}

SensorEDM::~SensorEDM()
{
  // (custom destructor to free dynamic memory)
}

void SensorEDM::setID(int myID)
{
  sensorID = myID;
}

void SensorEDM::writeOutput(
  std::ofstream& fileHandle, 
  DataHandler &inData,
  int smoke,
  int burn,
  int fire)
{
  // col 0
  fileHandle << inData.getTime() << ","; 

  // col 1 - 6
  fileHandle << inData.getDataValue(itemp) << ","; 
  fileHandle << inData.getDataValue(iO2) << ","; 
  fileHandle << inData.getDataValue(iCO) << ","; 
  fileHandle << inData.getDataValue(iCO2) << ","; 
  fileHandle << inData.getDataValue(iHCN) << ","; 
  fileHandle << inData.getDataValue(iflux) << ","; 

  // col 7 - 10
  fileHandle << sumFEDsmoke << ",";
  fileHandle << sumFEDheat[0] << ",";
  fileHandle << sumFEDheat[1] << ",";
  fileHandle << sumFEDheat[2] << ",";

  // col 11 - 13
  fileHandle << smoke << ",";
  fileHandle << burn << ",";
  fileHandle << fire << ",";

  // col 14
  fileHandle << inData.getStatus() << "\n"; 
}

void SensorEDM::updateTime(double time)
{
  // update the time increment
  dt = time - lastTime;
  dt = dt / 60.0;  // convert [sec] to [min]

  // store last time stamp
  lastTime = time;
}


// SMOKE TOXICITY
// use FED to check smoke toxicity
int SensorEDM::checkSmokeTox(DataHandler &inData)
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

  // init parameters
  int warning = 0;
  int use_fds = 0;
  double FED_CO, FED_CN, FED_NOx, FLD_irr, HV_CO2, FED_O2;

  // FED for carbon monoxide
  double CO = inData.getDataValue(iCO);
  FED_CO = 2.764 * pow(10.0, -5) * pow(CO, 1.036) * dt;

  // FED for CN which removes [NO2] and [NO] first
  // **note: we are not currently measuring [NO2] or [NO]
  double NO2, NO, CN;
  NO2 = 0.0;
  NO = 0.0;
  CN = inData.getDataValue(iHCN) - NO2 - NO;

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
  FED_O2 = dt / exp( 8.13 - 0.54*(20.9 - inData.getDataValue(iO2)) );

  // Hyperventilation Factor
  if (use_fds == 1)
  {
    // FDS
    HV_CO2 = (1.0 / 7.1) * exp(0.1903 * inData.getDataValue(iCO2) + 2.0004);
  }
  else
  {
    // SFPE
    HV_CO2 = exp(inData.getDataValue(iCO2) / 5.0);
  }

  // update the smoke toxicity FED sum 
  sumFEDsmoke += ((FED_CO + FED_CN + FED_NOx + FLD_irr) * HV_CO2 + FED_O2);

  // check for 1.0 FED threshold and/or severe oxygen depletion
  if (sumFEDsmoke >= FED_limit)
  {
    warning += 1;
  }
  if (inData.getDataValue(iO2) <= O2_limit)
  {
    warning += 1;
  }
  return warning;
}


// BURN THREATS
// use FED to check burn threats
int SensorEDM::checkBurnThreat(DataHandler &inData)
{
  // get new temperature and heat flux
  double temp = inData.getDataValue(itemp);
  double flux = inData.getDataValue(iflux);


  // 1. convection contribution
  // SFPE Handbook Eqn 63.45 (pain tolerance)
  double tconv1 = (2.0 * pow(10.0, 31) * pow(temp, -16.963)) + (4.0 * pow(10.0, 8) * pow(temp, -3.7561));
  double FEDconv1 = dt / tconv1;

  // SFPE Handbook Eqn 63.46
  double tconv2 = (5.0 * pow(10.0, 22) * pow(temp, -11.783)) + (3.0 * pow(10.0, 7) * pow(temp, -2.9636));
  double FEDconv2 = dt / tconv2;

  // SFPE Handbook Eqn 63.47
  double tconv3 = (2.0 * pow(10.0, 18) * pow(temp, -9.0403)) + (1.0 * pow(10.0, 8) * pow(temp, -3.10898));
  double FEDconv3 = dt / tconv3;


  // 2. radiation contribution 
  double minFlux = 2.5;
  double FEDrad1, FEDrad2, FEDrad3;
  if (flux < minFlux)
  {
    FEDrad1 = 0.0;
    FEDrad2 = 0.0;
    FEDrad3 = 0.0;
  }
  else
  {
    // tolerance limit, pain, 1st-degree burns
    double trad1 = 1.33 / pow(flux, 1.33);
    FEDrad1 = dt / trad1;
    
    // severe incapacitation, 2nd-degree burns
    double trad2 = 10.0 / pow(flux, 1.33);
    FEDrad2 = dt / trad2;

    // fatal exposure, 3rd-degree burns
    double trad3 = 16.7 / pow(flux, 1.33);      
    FEDrad3 = dt / trad3;
  }
  

  // cumulative FED
  sumFEDheat[0] += (FEDconv1 + FEDrad1);
  sumFEDheat[1] += (FEDconv2 + FEDrad2);
  sumFEDheat[2] += (FEDconv3 + FEDrad3);

  // warning check
  int warning = 0;
  for (int i = 0; i < maxBurn; i++)
  {
    if (sumFEDheat[i] >= FED_limit)
    {
      warning += 1;
    }
  }
  return warning;
}


// FIRE STATUS
// method for checking fire spread and flashover together
int SensorEDM::checkFireStatus(DataHandler& inData)
{
  // get the current temperature and heat flux
  double temperature = inData.getDataValue(itemp);
  double heatFlux = inData.getDataValue(iflux);

  // perform hazard detection calculations
  int warning = 0;
  if (fireStatus < maxFire)
  {
    for (int i = 0; i < maxFire; i++)
    {
      if (temperature > tempLimits[i] && heatFlux > fluxLimits[i])
      {
        warning += 1;
      }
    }
    fireStatus = std::max(fireStatus, warning);
  }
  return fireStatus;
}


// DAMAGED SENSOR
int SensorEDM::handleDamagedSensor(int flag)
{
  // flag = 0 --> set fire status
  // flag = 1 --> set burn threats
  // flag = 2 --> set smoke toxicity
  int warning = 0;
  if (flag == 0)
  {    
    // fire status
    warning = maxFire;
  }
  else if (flag == 1)
  {
    // burn threats
    warning = maxBurn;
  }
  else if (flag == 2)
  {
    // smoke toxicity
    warning = maxSmoke;
  }
  return warning;
}

