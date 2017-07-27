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

// additional LCM directives
#include <lcm/lcm-cpp.hpp>
#include "send_to_edm/data_to_edm.hpp"

// include my custom classes
#include "DataHandler.h"
#include "Sensor.h"

// namespace declarations
using namespace std;


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
  const int MAX_MSG_LIMIT = 5;

  //===========================================================================

  // init
  int i;
  int room = 0;
  int numMsgRecv = 0;

  // warning arrays
  int flashover[NUM_ROOMS];

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

      // distribute new data to each sensor
      for (i = 0; i < NUM_ROOMS; i++)
      {
        sensorArray[i].setData(0, currentData.getTime());
        sensorArray[i].setData(1, currentData.getTemp(i));
        sensorArray[i].setData(2, currentData.getO2(i));
        sensorArray[i].setData(3, currentData.getCO(i));
        sensorArray[i].setData(4, currentData.getCO2(i));
        sensorArray[i].setData(5, currentData.getHCN(i));
        sensorArray[i].setData(6, currentData.getFlux(i));
      }

      // check the hazards at each sensor location
      for (i = 0; i < NUM_ROOMS; i++)
      {

        // FLASHOVER
        // Fire Signatures: temperature, heat flux
        flashover[i] = sensorArray[i].checkFlashover();
        std::cout << "room #" << i << " flashover check = " << flashover[i] << std::endl;

        // BURN THREATS
        // Fire Signatures: heat flux, O2

        // SMOKE TOXICITY
        // Fire Signatures: O2, CO, HCN, temperature

        // FIRE SPREAD
        // Fire Signatures: temperature, O2, CO, CO2, 

      }

    }
  }

  printf("exit EDM main\n");
  return 0;
}
