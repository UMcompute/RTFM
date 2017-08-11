#include <iostream>
#include <stdio.h>

#include "Sensor.h"

#define NUM_ROOMS 1
#define NUM_DATA 7

// UNIT TEST PROGRAM
int main(int argc, char** argv) 
{

  const int N = 6;
  // input time in sec
  double time[N] = {60.0, 120.0, 180.0, 240.0, 300.0, 360.0};
  // input temperature in degrees C
  double temp[N] = {20.0, 65.0, 125.0, 220.0, 405.0, 405.0};
  // input O2 in [%]
  double O2[N] = {20.9, 20.9, 19.0, 17.5, 15.0, 12.0};
  // input CO in [ppm]
  double CO[N] = {0.0, 0.0, 500.0, 2000.0, 3500.0, 6000.0};
  // input CO2 in [%]
  double CO2[N] = {0.0, 0.0, 1.5, 3.5, 6.0, 8.0};
  // input HCN in [ppm]
  double HCN[N] = {0.0, 0.0, 50.0, 150.0, 250.0, 300.0};
  // input flux in kW/m^2
  double flux[N] = {0.0, 0.1, 0.4, 1.0, 2.5, 2.5};

  int i, j;
  int burnThreat[NUM_ROOMS];
  int smokeToxicity[NUM_ROOMS];
  int fireSpread[NUM_ROOMS];
  int flashover[NUM_ROOMS];

  // create new Sensor class objects based on the number of rooms
  Sensor sensorArray[NUM_ROOMS];
  for (i = 0; i < NUM_ROOMS; i++)
  {
    sensorArray[i].setID(i);
  }  

  for (i = 0; i < N; i++)
  {
    //printf("t = %f, T = %f, q = %f \n", time[i], temp[i], flux[i]);
    printf("t = %f \n", time[i]);

    for (j = 0; j < NUM_ROOMS; j++)
    {
      // update sensor data
      sensorArray[j].setData(0, time[i]);
      sensorArray[j].setData(1, temp[i]);
      sensorArray[j].setData(2, O2[i]);
      sensorArray[j].setData(3, CO[i]);
      sensorArray[j].setData(4, CO2[i]);
      sensorArray[j].setData(5, HCN[i]);
      sensorArray[j].setData(6, flux[i]);

      burnThreat[j] = sensorArray[j].checkBurnThreat();
      smokeToxicity[j] = sensorArray[j].checkSmokeTox();

      fireSpread[j] = sensorArray[j].checkFireSpread();
      flashover[j] = sensorArray[j].checkFlashover();

      /*
      if (fireSpread[j] == 1)
      {
        flashover[j] = sensorArray[j].checkFlashover();
      }
      else
      {
        flashover[j] = 0
      }
      */
      
      sensorArray[j].updateTime();

    }

  }

  return 0;
}