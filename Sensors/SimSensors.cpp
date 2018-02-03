// C++ directives
#include <math.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
#include <queue>
#include <vector>
#include <string>
#include <stdio.h>
#include <fstream>

// LCM directives
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// my new directives
#include "SensorEvent.h"
#include "Sensor.h"


// This overloaded operator is needed for the priority queue 
// to sort events by ascending time.
bool operator>(
  const SensorEvent& lhs, 
  const SensorEvent& rhs)
{
  return (lhs.getTime() > rhs.getTime());
}


// Returns a random number between 0.0 and 1.0 (uniform dist).
double getRandDble()
{
  double p = 0.0;
  p = ((double)((rand() % 1000000) / 1000000.0));
  return p;
}


// A unit test using data from SFPE Handbook
void runUnitTest(
  lcm::LCM& lcmHandle,
  const int numSensors);


// MAIN SENSOR SIMULATOR PROGRAM
int main(int argc, char* argv[])
{

  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }

  // INPUT ================================================
  int numSensors, unitTest;
  double tmax, tnom, failureProb;
  // get input file from command line argument
  std::ifstream inFile;
  std::string inFileName;
  if (argc != 2)
  {
    printf("***Error: only supply one command line argument\n");
    printf("   Expected usage:  $ ./SimSensors.ex <input_file>\n");
    return 1;
  }
  else
  {
    inFileName = argv[1];
    printf("\n%s has input file: %s \n", argv[0], inFileName.c_str());
  }
  // read the four input values needed
  inFile.open(inFileName.c_str());
  inFile >> numSensors;
  inFile >> tmax;
  inFile >> tnom;
  inFile >> failureProb;
  inFile >> unitTest;
  inFile.close();
  // ======================================================

  // initialize the sensor simulator
  printf("\n\t{Started Sensor Simulator}\n");
  srand(2);
  int sid; 
  int numFailed = 0;
  double sleepConversion = pow(10.0, 6.0);
  double time = 0.0;
  double dtMin = 0.5;
  double dt, st, myTime, failCheck;

  // initialize the LCM data structures
  std::string channelPrefix = "SENSOR";
  std::string channel;
  sensor::sensor_data dataToSend;
  Sensor *sensorArray;
  sensorArray = new Sensor [numSensors];

  // declare the primary queue for sensorEvent events
  std::priority_queue< SensorEvent, std::vector<SensorEvent>, std::greater<SensorEvent> > eventQueue;

  // Initialize the queue with the first data measurement events
  //  for each sensor (for the normal sensor simulation) ...
  if (unitTest == 0)
  {
    for (int i = 0; i < numSensors; i++)
    {
      myTime = getRandDble() * tnom;
      eventQueue.push( SensorEvent(i, myTime) );
    }
  }
  // ... or perform unit test to assess system:
  else if (unitTest == 1)
  {
    runUnitTest(lcm, numSensors);
  }
  else
  {
    printf("(there was likely an error reading the last line of the input file)\n");
    return 2;
  }

  // initialize the sensor array for storing current data measurements
  for (int i = 0; i < numSensors; i++)
  {
    sensorArray[i].setID(i);
  }
  int NDATA = sensorArray[0].getNDATA();

  //-------------------------------------------------------
  // handle the event queue to send messages
  while (!eventQueue.empty())
  {
    // handle the sensorEvent event
    sid = eventQueue.top().getID();
    st = eventQueue.top().getTime();
    usleep( (st - time) * sleepConversion);
    time = st;
    eventQueue.pop();

    // test if sensor has failed
    if ( sensorArray[sid].getActive() )
    {
      failCheck = getRandDble();
      if (failCheck < failureProb)
      {
        printf("\n***sensor #%d FAILED at time = %f sec***\n", sid, time);
        sensorArray[sid].setActive(false);
        numFailed += 1;
        for (int j = 0; j < NDATA; j++)
        {
          sensorArray[sid].setData(j, -1.0);
        }
      }
      else
      {
        // sensor #sid records new data at time
        for (int j = 0; j < NDATA; j++)
        {
          sensorArray[sid].setData(j, 1.0);
        }
      }
    }

    // send current data
    sensorArray[sid].fillDataContainer(time, dataToSend);
    channel = channelPrefix + std::to_string(sid);
    lcm.publish(channel, &dataToSend);

    // add a new event to the sensor queue
    dt = getRandDble() * tnom + dtMin;
    if ( (time + dt) < tmax)
    {
      eventQueue.push( SensorEvent(sid, time + dt) );
    }
  }
  //-------------------------------------------------------

  
  // print summary statistics
  printf("\n\t{Sensor Simulation Summary}\n");
  printf("\t  %d sensors failed\n", numFailed);
  printf("\t  %d total sensors\n", numSensors);
  printf("\t  %.2f percent failure rate\n", ( (double)numFailed / (double)numSensors) * 100.0);
  printf("\t  %.3f total time [sec]\n\n", time );

  // free dynamic memory
  delete [] sensorArray;

  // exit the main program
  return 0;
}


// A unit test using data from SFPE Handbook
void runUnitTest(lcm::LCM& lcmHandle, const int numSensors)
{
  printf("\n\t{UNIT TEST USING %d SENSORS}\n", numSensors);

  // used for usleep function:
  double sleepTime = 0.1 * pow(10.0, 6.0);

  // N is the number of sensor measurements taken over time
  const int N = 6;
  // input time in sec
  double time[N] = {60.0, 120.0, 180.0, 240.0, 300.0, 360.0};
  // input temperature in degrees C
  double temp[N] = {20.0, 65.0, 125.0, 220.0, 405.0, 405.0};
  // input flux in kW/m^2
  double flux[N] = {0.0, 0.1, 0.4, 1.0, 2.5, 2.5};
  // input O2 in [%]
  double O2[N] = {20.9, 20.9, 19.0, 17.5, 15.0, 12.0};
  // input CO in [ppm]
  double CO[N] = {0.0, 0.0, 500.0, 2000.0, 3500.0, 6000.0};
  // input CO2 in [%]
  double CO2[N] = {0.0, 0.0, 1.5, 3.5, 6.0, 8.0};
  // input HCN in [ppm]
  double HCN[N] = {0.0, 0.0, 50.0, 150.0, 250.0, 300.0};
  // prefix fo the LCM data channel that these messages will use
  std::string channelPrefix = "SENSOR";

  // complete this test using four sensors as an example
  Sensor *sensorArray;
  sensorArray = new Sensor [numSensors];
  for (int i = 0; i < numSensors; i++)
  {
    sensorArray[i].setID(i);
  }

  // data measurement mapping:
  //    0 = temp
  //    1 = flux
  //    2 = O2
  //    3 = CO
  //    4 = CO2
  //    5 = HCN

  // simple time step loop
  std::string channel;
  sensor::sensor_data dataToSend;
  for (int n = 0; n < N; n++)
  {
    printf("  time = %f\n", time[n]);
    for (int i = 0; i < numSensors; i++)
    {
      //printf("\tsensor i = %d\n", i);
      usleep(sleepTime);
      // sensor #i must set its SIX data values
      //   (every sensor in this test will send the same values
      //    at the same time)
      sensorArray[i].setData(0, temp[n] );
      sensorArray[i].setData(1, flux[n] );
      sensorArray[i].setData(2, O2[n] );
      sensorArray[i].setData(3, CO[n] );
      sensorArray[i].setData(4, CO2[n] );
      sensorArray[i].setData(5, HCN[n] );

      /*
      // print sensorArray[i] data array:
      int NDATA = sensorArray[i].getNDATA();
      printf("\t");
      for (int j = 0; j < NDATA; j++)
      {
        printf("%.2f\t", sensorArray[i].getData(j));
      }
      printf("\n");
      */

      // send current data
      sensorArray[i].fillDataContainer(time[n], dataToSend);
      channel = channelPrefix + std::to_string(i);
      lcmHandle.publish(channel, &dataToSend);
      printf("\t*published message on %s*\n\n", channel.c_str() );
    }
  }

  // free dynamic memory
  delete [] sensorArray;

  // exit unit test
  printf("\t{END UNIT TEST}\n");
}
