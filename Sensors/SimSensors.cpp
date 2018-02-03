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


// MAIN SENSOR SIMULATOR PROGRAM
int main(int argc, char* argv[])
{

  // INPUT ================================================
  int numSensors;
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

  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }

  // initialize the queue and sensor array
  for (int i = 0; i < numSensors; i++)
  {
    myTime = getRandDble() * tnom;
    eventQueue.push( SensorEvent(i, myTime) );
    sensorArray[i].setID(i);
  }
  int NDATA = sensorArray[0].getNDATA();

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