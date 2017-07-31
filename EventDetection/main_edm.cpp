/*
    $ lcm-gen -x ../RTFM/data_edm.lcm
    $ g++ main_edm.cpp -llcm -std=c++11
    $ ./a.out
*/

// C++ preprocessor directives
#include <iostream>
#include <stdio.h>
#include <queue>
#include <sys/select.h>
#include <ctime>
#include <math.h>
#include <unistd.h>
#include <chrono>
#include <fstream>

// additional LCM directives
#include <lcm/lcm-cpp.hpp>
#include "send_to_edm/data_to_edm.hpp"

// include my custom classes
#include "DataHandler.h"
#include "Sensor.h"


//const int NUM_ROOMS = 4;
#define NUM_ROOMS 4
/* ====================================
    ASSUMPTION: one sensor per room
==================================== */


//const int NUM_DATA = 7;
#define NUM_DATA 7
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


// MAIN PROGRAM
int main(int argc, char** argv) {
  printf("starting EDM main...\n");

  // input
  const int MAX_MSG_LIMIT = 30;

  //===========================================================================

  // init
  int i;
  int room = 0;
  int numMsgRecv = 0;

  // warning arrays
  int flashover[NUM_ROOMS];
  int burnThreat[NUM_ROOMS];
  int smokeToxicity[NUM_ROOMS];
  int fireSpread[NUM_ROOMS];

  // testing output
  std::ofstream outFile1;
  std::ofstream outFile2;
  std::ofstream outFile3;
  outFile1.open("temp-flux.txt");
  outFile2.open("time-flashover.txt");
  outFile3.open("time-burn-FEDs.txt");

  // construct LCM and check if it is good!
  lcm::LCM lcm;
  if(!lcm.good()) return 1;

  // construct a Handler and subsribe to receive messages
  DataHandler currentData;
  lcm.subscribe("EDM_CHANNEL", &DataHandler::handleMessage, &currentData);

  // create new Sensor class objects based on the number of rooms
  Sensor sensorArray[NUM_ROOMS];
  for (i = 0; i < NUM_ROOMS; i++)
  {
    sensorArray[i].setID(i);
  }

  // MAIN event loop
  while (numMsgRecv < MAX_MSG_LIMIT)
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

    // interpret status
    if (0 == status)
    {
      // no msg yet!
      printf("\n   [waiting for msg in EDM main loop]\n");
    }
    else if (FD_ISSET(lcm_fd, &fds))
    {
      // LCM has events for you to process!
      lcm.handle();
      numMsgRecv += 1;

      // check the hazards at each sensor location
      for (i = 0; i < NUM_ROOMS; i++)
      {
        // distribute new data to each sensor
        sensorArray[i].setData(0, currentData.getTime());
        sensorArray[i].setData(1, currentData.getTemp(i));
        sensorArray[i].setData(2, currentData.getO2(i));
        sensorArray[i].setData(3, currentData.getCO(i));
        sensorArray[i].setData(4, currentData.getCO2(i));
        sensorArray[i].setData(5, currentData.getHCN(i));
        sensorArray[i].setData(6, currentData.getFlux(i));

        // FLASHOVER
        flashover[i] = sensorArray[i].checkFlashover();

        if (i == 0)
        {
          outFile1 << currentData.getTemp(i) << ", " << currentData.getFlux(i) << "\n";
          outFile2 << currentData.getTime() << ", " << flashover[i] << "\n";
        }

        // SMOKE TOXICITY
        smokeToxicity[i] = sensorArray[i].checkSmokeTox();

        // BURN THREATS
        burnThreat[i] = sensorArray[i].checkBurnThreat();

        if (i == 0)
        {
          outFile3 << currentData.getTime() << ", " << burnThreat[i] << ", " << sensorArray[i].getFEDvals(1) << ", " << sensorArray[i].getFEDvals(2) << "\n";
        }

        // FIRE SPREAD
        fireSpread[i] = sensorArray[i].checkFireSpread();

        // TIME UPDATE
        sensorArray[i].updateTime();
      }
    }
  }

  outFile1.close();
  outFile2.close();
  outFile3.close();

  printf("exit EDM main\n");
  return 0;
}
