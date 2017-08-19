#include <iostream>
#include <stdio.h>
#include <fstream>

#include "Sensor.h"

#define NUM_ROOMS 1
#define NUM_DATA 7

// UNIT TEST PROGRAM
int main(int argc, char** argv) 
{

  int print_output = 1;
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
  int fireStatus[NUM_ROOMS];
  //int fireSpread[NUM_ROOMS];
  //int flashover[NUM_ROOMS];

  // preparation for output
  double FED_smoke, FED_heat_pain, FED_heat_fatal;
  std::ofstream outFile[NUM_ROOMS];
  std::string file_prefix = "edm_output_";
  std::string file_suffix = ".csv";
  std::string file_name;
  if (print_output == 1)
  {
    for (i = 0; i < NUM_ROOMS; i++)
    {
      file_name = file_prefix + std::to_string(i) + file_suffix;
      std::cout << file_name << "\n";
      outFile[i].open(file_name.c_str());
    }
  }  

  // create new Sensor class objects based on the number of rooms
  Sensor sensorArray[NUM_ROOMS];
  for (i = 0; i < NUM_ROOMS; i++)
  {
    sensorArray[i].setID(i);
  }  

  for (i = 0; i < N; i++)
  {
    printf("time = %f min \n", time[i]/60.0);

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

      // check all hazards
      burnThreat[j] = sensorArray[j].checkBurnThreat();
      smokeToxicity[j] = sensorArray[j].checkSmokeTox();
      fireStatus[j] = sensorArray[j].checkFireStatus();
      //fireSpread[j] = sensorArray[j].checkFireSpread();
      //flashover[j] = sensorArray[j].checkFlashover();
      sensorArray[j].updateTime();

      // print FED results
      printf("  FED Smoke Tox  = %.2f \n", sensorArray[j].getFEDvals(0));
      printf("  FED Heat Pain  = %.2f \n", sensorArray[j].getFEDvals(1));
      printf("  FED Heat Fatal = %.2f \n", sensorArray[j].getFEDvals(2));

      // write to specific room file 
      outFile[j] << time[i] << "," << temp[i] << "," << O2[i] << ","; 
      outFile[j] << CO[i] << "," << CO2[i] << "," << HCN[i] << "," << flux[i] << ",";
      outFile[j] << sensorArray[j].getFEDvals(0) << "," << sensorArray[j].getFEDvals(1) << "," << sensorArray[j].getFEDvals(2) << ",";
      outFile[j] << smokeToxicity[j] << "," << burnThreat[j] << ",";
      outFile[j] << fireStatus[j] << "\n";

    }

  }

  // close the testing files
  if (print_output == 1)
  {
    for (i = 0; i < NUM_ROOMS; i++)
    {
      outFile[i].close();
    }
  }

  return 0;
}