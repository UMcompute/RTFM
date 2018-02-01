// typical C++ directives
#include <stdio.h>

// directives needed for LCM work
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"
#include "DataHandler.h"


// This function checks if a new LCM message is available 
//   (it returns TRUE if there IS a new message, which then
//   must be handled properly with "lcm.handle()").
bool checkForNewMsg(lcm::LCM &lcm)
{

  // setup the LCM file descriptor for waiting
  int lcm_fd = lcm.getFileno();
  fd_set fds;
  FD_ZERO(&fds);
  FD_SET(lcm_fd, &fds);

  // wait a limited amount of time for an incoming msg
  struct timeval timeout = {
    1,  // seconds
    0   // microseconds
  };
  int status = select(lcm_fd + 1, &fds, 0, 0, &timeout);

  // interpret the file descriptor status
  if (0 == status)
  {
    return false;
  }
  else if (FD_ISSET(lcm_fd, &fds))
  {
    return true;
  }
}




/*
// C++ preprocessor directives
#include <iostream>
#include <queue>
#include <sys/select.h>
#include <sys/time.h>
#include <time.h>
#include <ctime>
#include <math.h>
#include <unistd.h>
#include <chrono>
#include <fstream>
#include <string>

//#include "send_to_edm/data_to_edm.hpp"

// include my custom classes

#include "Sensor.h"
*/

//const int NUM_ROOMS = 4;
//#define NUM_ROOMS 4
/* ====================================
    ASSUMPTION: one sensor per room
==================================== */


//const int NUM_DATA = 7;
//#define NUM_DATA 7
/* ====================================
    DATA KEY: sensorData[i]
    i | parameter
    0 = time
    1 = upper layer gas temperature
    2 = O2
    3 = CO
    4 = CO2
    5 = HCN
    6 = heat flux
==================================== */


// MAIN EVENT DETECTION MODEL
int main(int argc, char** argv) 
{

  // INPUT ============================
  const double maxTime = 20.0;
  // ==================================

  printf("\n    {Started Event Detection Model}\n");

  // initiate LCM and check if it is working
  lcm::LCM lcm;
  if(!lcm.good()) return 1;

  // construct a Handler and subsribe to receive messages from main RTFM
  DataHandler currentData;
  lcm.subscribe("EDM_CHANNEL", &DataHandler::handleMessage, &currentData);

  // main time loop
  double currentTime = 0.0;
  while (currentTime < maxTime)
  {
    if ( checkForNewMsg(lcm) )
    {
      // if true, a new message has been sent via LCM
      lcm.handle();
      currentTime = currentData.getTime();
    }
  }  // end main time loop

  printf("\n\n    {End of Event Detection Model}\n");

  return 0;




  /*    OLD STUFF 
  
  printf("\t\tEDM currentTime: %f\n", currentTime);
  // input
  const double TIME_MAX = 10.0;

  //===========================================================================

  // init
  int i;
  int room = 0;
  int numMsgRecv = 0;
  int msgFromEachSensor[NUM_ROOMS];
  int msgLimit = 38528;

  // warning arrays
  int burnThreat[NUM_ROOMS];
  int smokeToxicity[NUM_ROOMS];
  int fireStatus[NUM_ROOMS];

  // preparation for output
  int print_output = 0;
  double t, T, O2, CO, CO2, HCN, Q; 
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

  // timer setup
  char buffer[26];
  int millisec;
  struct tm* tm_info;
  struct timeval tv;  

  





  // create new Sensor class objects based on the number of rooms
  Sensor sensorArray[NUM_ROOMS];
  for (i = 0; i < NUM_ROOMS; i++)
  {
    sensorArray[i].setID(i);
    msgFromEachSensor[i] = 0;
  }

  // official start time
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
  std::chrono::steady_clock::time_point current;

  // MAIN event loop
  xxxxxxxxxxxxxxxxxxx  t = 0.0;
  //while (numMsgRecv < msgLimit)
  xxxxxxxxxxxxxxxxxxx  while (t < TIME_MAX)
  {



      numMsgRecv += 1;

      // update data for the current sensor
      i = currentData.getRoom();
      msgFromEachSensor[i] += 1;
      sensorArray[i].setData(0, currentData.getTime());
      sensorArray[i].setData(1, currentData.getTemp());
      sensorArray[i].setData(2, currentData.getO2());
      sensorArray[i].setData(3, currentData.getCO());
      sensorArray[i].setData(4, currentData.getCO2());
      sensorArray[i].setData(5, currentData.getHCN());
      sensorArray[i].setData(6, currentData.getFlux());

      // SMOKE TOXICITY
      smokeToxicity[i] = sensorArray[i].checkSmokeTox();

      // BURN THREATS
      burnThreat[i] = sensorArray[i].checkBurnThreat();

      // FIRE STATUS
      fireStatus[i] = sensorArray[i].checkFireStatus();

      // TIME UPDATE
      sensorArray[i].updateTime();

      // PRINT OUTPUT
      if (print_output == 1)
      {
        // raw data
        t = currentData.getTime();
        T = currentData.getTemp();
        O2 = currentData.getO2();
        CO = currentData.getCO();
        CO2 = currentData.getCO2();
        HCN = currentData.getHCN();
        Q = currentData.getFlux();

        // output
        FED_smoke = sensorArray[i].getFEDvals(0);
        FED_heat_pain = sensorArray[i].getFEDvals(1);
        FED_heat_fatal = sensorArray[i].getFEDvals(2);

        // write to specific room file 
        outFile[i] << t << "," << T << "," << O2 << ","; 
        outFile[i] << CO << "," << CO2 << "," << HCN << "," << Q << ",";
        outFile[i] << FED_smoke << "," << FED_heat_pain << "," << FED_heat_fatal << ",";
        outFile[i] << smokeToxicity[i] << "," << burnThreat[i] << ",";
        outFile[i] << fireStatus[i] << "\n";
      }

      //=================================
      // new timer
      gettimeofday(&tv, NULL);
      millisec = lrint(tv.tv_usec/1000.0); // Round to nearest millisec
      if (millisec>=1000) 
      {
        // Allows for rounding up to nearest second
        millisec -=1000;
        tv.tv_sec++;
      }
      tm_info = localtime(&tv.tv_sec);
      strftime(buffer, 26, "%H:%M:%S", tm_info);
      //printf("sensor #%d checks finished at msg #%d time %s.%03d\n", i, msgFromEachSensor[i], buffer, millisec);
      printf("%d, %d, %s.%03d \n", i, msgFromEachSensor[i], buffer, millisec);
      //=================================
      
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
  */  
}
