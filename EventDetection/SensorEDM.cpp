#include "SensorEDM.h"
#include "DataHandler.h"
#include <math.h>

//#include <iostream>
//#include <stdio.h>


SensorEDM::SensorEDM()
{
  // FIRE STATUS
  fireStatus = 0;

  /*
  lastTemp = 20.0;

  // initial values of computed hazards
  lastTime = 0.0;
  lastTemp = 20.0;
  sumFEDheat1 = 0.0;
  sumFEDheat2 = 0.0;
  sumFEDsmoke = 0.0;

  std::cout << "new sensor created" << std::endl;
  */

}

SensorEDM::~SensorEDM()
{
  // (custom destructor to free dynamic memory)
}

void SensorEDM::setID(int myID)
{
  sensorID = myID;
}

/*
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

*/




// // Tested 08-10-17 at 11:45 with SFPE Handbook Table 63.22
// int Sensor::checkSmokeTox()
// {
//   /* *** CHECK UNITS OF ALL DATA USED IN THIS FUNCTION! ***
//     O2 [%]
//     CO [ppm]
//     CO2 [%]
//     HCN [ppm]

//     For example, in the case of [%], use the "number":
//       if equation contains something like this: (20.9 - [O2])
//       then say [O2] = 16.5%, 
//       then use "16.5" directly in the equation: (20.9 - 16.5)
//   */
//   int warning = 0;
//   int use_fds = 0;
//   double FED_CO, FED_CN, FED_NOx, FLD_irr, HV_CO2, FED_O2;
//   double O2_limit = 7.0; // [%] (Alarie 2002)
//   double FED_limit = 1.0;

//   // update time step
//   double dt = (sensorData[itime] - lastTime) / 60.0;  // converted [sec] to [min]

//   // FED for carbon monoxide
//   FED_CO = 2.764 * pow(10.0, -5) * pow(sensorData[iCO], 1.036) * dt;

//   // FED for CN which removes [NO2] and [NO] first
//   // **note: we are not currently measuring [NO2] or [NO]
//   double NO2, NO, CN;
//   NO2 = 0.0;
//   NO = 0.0;
//   CN = sensorData[iHCN] - NO2 - NO;

//   // use either the FDS or SFPE equation for [CN] exposure-dose
//   if (use_fds == 1)
//   {
//     // FDS Eq. 17.20
//     FED_CN = ((1.0 / 220.0) * exp(CN / 43.0) - 0.0045) * dt;
//   }
//   else
//   {
//     // SFPE Eq. 63.24
//     FED_CN = ( pow(CN, 2.36) / 1200000.0 ) * dt;
//   }

//   // FED for any [NOx] present
//   // **note: currently not measuring any [NOx]
//   FED_NOx = 0.0;

//   // FLD for irritants (none currently)
//   // future: include HCl, HBr, formaldehyde, acrolein, HF, etc.
//   FLD_irr = 0.0;

//   // FED for O2 depletion
//   double O2 = sensorData[iO2];  // [%]
//   FED_O2 = dt / exp( 8.13 - 0.54*(20.9 - O2) );

//   // Hyperventilation Factor
//   if (use_fds == 1)
//   {
//     // FDS
//     HV_CO2 = (1.0 / 7.1) * exp(0.1903 * sensorData[iCO2] + 2.0004);
//   }
//   else
//   {
//     // SFPE
//     HV_CO2 = exp(sensorData[iCO2] / 5.0);
//   }

//   // update the smoke toxicity FED sum 
//   sumFEDsmoke += ((FED_CO + FED_CN + FED_NOx + FLD_irr) * HV_CO2 + FED_O2);

//   // check for 1.0 FED threshold and/or severe oxygen depletion
//   if (sumFEDsmoke >= FED_limit)
//   {
//     warning += 1;
//   }
//   if (O2 <= O2_limit)
//   {
//     warning += 1;
//   }
//   /*
//   // print output for unit test
//   printf("  FED_CO = %6.2f\n", FED_CO);
//   printf("  FED_CN = %6.2f\n", FED_CN);
//   printf("  FED_O2 = %6.2f\n", FED_O2);
//   printf("  HV_CO2 = %6.2f\n", HV_CO2);
//   printf("  FEDtot = %6.2f\n", sumFEDsmoke);
//   */
//   return warning;
// }


// // Tested 08-10-17 at 09:00 with SFPE Handbook Table 63.22
// int Sensor::checkBurnThreat()
// {
//   // warning initialization
//   int warning = 0;
//   double FED_limit = 1.0;

//   // dt update
//   double dt = (sensorData[itime] - lastTime) / 60.0;  // converted [sec] to [min]

//   // convection contribution
//   double temp = sensorData[itemp];
//   double tc1, tc2, FED_c1, FED_c2;
//   double A1, B1, A2, B2;
//   A1 = 2.0 * pow(10.0, 31);
//   B1 = 4.0 * pow(10.0, 8);
//   A2 = 2.0 * pow(10.0, 18);
//   B2 = 1.0 * pow(10.0, 8);
//   tc1 = A1 * pow(temp, -16.963) + B1 * pow(temp, -3.7561);
//   tc2 = A2 * pow(temp, -9.0403) + B2 * pow(temp, -3.10898);
//   FED_c1 = dt / tc1;
//   FED_c2 = dt / tc2;

//   // radiation contribution
//   double flux = sensorData[iflux];
//   double tr1, tr2, FED_r1, FED_r2;
//   double r1, r2;
//   double minFlux = 2.5;
//   r1 = 1.33;
//   r2 = 16.7;
//   if (flux < minFlux)
//   {
//     tr1 = 0.0;
//     tr2 = 0.0;
//     FED_r1 = 0.0;
//     FED_r2 = 0.0;
//   }
//   else
//   {
//     tr1 = r1 / pow(flux, 1.33);
//     tr2 = tr1 * (r2 / r1);
//     FED_r1 = dt / tr1;
//     FED_r2 = dt / tr2;
//   }

//   // summation of FED
//   sumFEDheat1 += (FED_c1 + FED_r1);
//   sumFEDheat2 += (FED_c2 + FED_r2);

//   // warning check
//   if (sumFEDheat1 >= FED_limit)
//   {
//     warning += 1;
//   }
//   if (sumFEDheat2 >= FED_limit)
//   {
//     warning += 1;
//   }
//   /*
//   // print output for unit test
//   printf("FED for pain: \n");
//   printf("  convection = %8.2f\n", FED_c1);
//   printf("  raditation = %8.2f\n", FED_r1);
//   printf("  FEDpain(t) = %8.2f\n", FED_c1 + FED_r1);
//   printf("  FEDsum(t)  = %8.2f\n", sumFEDheat1);
//   printf("FED for full-thickness burns: \n");
//   printf("  convection = %8.2f\n", FED_c2);
//   printf("  raditation = %8.2f\n", FED_r2); 
//   printf("  FEDfull(t) = %8.2f\n", FED_c2 + FED_r2);
//   printf("  FEDsum(t)  = %8.2f\n", sumFEDheat2);
//   */
//   return warning;
// }


// FIRE STATUS
// method for checking fire spread and flashover together
int SensorEDM::checkFireStatus(DataHandler& inData)
{
  // set limits for:
  //    1. fire spread to compartment
  //    2. flashover in compartment 
  int warning = 0;

  // get the current temperature and heat flux
  double temperature = inData.getDataValue(itemp);
  double heatFlux = inData.getDataValue(iflux);

  // perform hazard detection calculations
  if (fireStatus < maxWarning)
  {
    for (int i = 0; i < maxWarning; i++)
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
