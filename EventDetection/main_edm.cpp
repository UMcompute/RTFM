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

// namespace declarations
using namespace std;

// global constants
const int NUM_ROOMS = 4;
const int NUM_DATA = 7;


// LCM class for receiving message data
class DataHandler
{

  private:
    int my_num_rooms;
    double my_time_stamp;
    double my_temperature[NUM_ROOMS];
    double my_O2_conc[NUM_ROOMS];
    double my_CO_conc[NUM_ROOMS];
    double my_CO2_conc[NUM_ROOMS];
    double my_HCN_conc[NUM_ROOMS];
    double my_heat_flux[NUM_ROOMS];

  public:
    ~DataHandler() {}

    void handleMessage(const lcm::ReceiveBuffer* rbuf,
  		     const std::string& chan,
  		     const send_to_edm::data_to_edm* msg)
    {
      // assign incoming data to proper local memory
      int i;
      my_num_rooms = msg->num_rooms;
      my_time_stamp = msg->time_stamp;
      for (i = 0; i < my_num_rooms; i++)
      {
        my_temperature[i] = msg->temperature[i];
        my_O2_conc[i] = msg->O2_conc[i];
        my_CO_conc[i] = msg->CO_conc[i];
        my_CO2_conc[i] = msg->CO2_conc[i];
        my_HCN_conc[i] = msg->HCN_conc[i];
        my_heat_flux[i] = msg->heat_flux[i];
      }
    }
  
    // get functions to return value at provided room index
    double getTime()            {   return my_time_stamp;           }
    double getTemp(int index)   {   return my_temperature[index];   }
    double getO2(int index)     {   return my_O2_conc[index];       }
    double getCO(int index)     {   return my_CO_conc[index];       }
    double getCO2(int index)    {   return my_CO2_conc[index];      }
    double getHCN(int index)    {   return my_HCN_conc[index];      }
    double getFlux(int index)   {   return my_heat_flux[index];     }
  
};


// Sensor class to store data on per room basis
class Sensor
{
  private:
    int roomID;
    double sensorData[NUM_DATA];
  public:
    Sensor()
    {
      int i;
      for (i = 0; i < NUM_DATA; i++)
      {
        sensorData[i] = 0.0;
      }
      cout << "new sensor created" <<  endl;
    }
    ~Sensor()
    {
      cout << "deleted a sensor" << endl;
    }
    void setID(int myID)
    {
      roomID = myID;
      cout << "my room id is " << roomID << endl;
    }
};




// MAIN PROGRAM
int main(int argc, char** argv) {
  
  printf("starting EDM main...\n");

  // input
  const int MAX_MSG_LIMIT = 1000;

  //===========================================================================

  // init
  int i;
  int room = 0;
  int numMsgRecv = 0;

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

      // check the getter functions
      cout << currentData.getTime() << endl;
      cout << currentData.getTemp(room) << endl;
      cout << currentData.getO2(room) << endl;
      cout << currentData.getCO(room) << endl;
      cout << currentData.getCO2(room) << endl;
      cout << currentData.getHCN(room) << endl;
      cout << currentData.getFlux(room) << endl;

      // FLASHOVER

      // BURN THREATS

      // SMOKE TOXICITY

    }
  }

  printf("exit EDM main\n");
  return 0;
}
