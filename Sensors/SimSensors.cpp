// C++ directives
#include <math.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
#include <queue>
#include <vector>
#include <string>

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

  // INPUT ============================
  // (move this into an input file?)
  const int numSensors = 4;
  const double tnom = 2.5;
  const double tmax = 11.0;
  const double failureProb = 0.40;
  // ==================================

  std::cout << "\n    {Started Sensor Simulator}\n";

  srand(1000);
  int sid; 
  int numFailed = 0;
  double sleepConversion = pow(10.0, 6.0);
  double time = 0.0;
  double dt, st, myTime, failCheck;

  sensor::sensor_data dataToSend;
  Sensor sensorArray[numSensors];
  std::string channelPrefix = "SENSOR";
  std::string channel;

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
        std::cout << "\n***sensor #" << sid << " FAILED at time = " << time << " sec\n";
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
    dt = (getRandDble() * tnom) + tnom;
    if ( (time + dt) < tmax)
    {
      eventQueue.push( SensorEvent(sid, time + dt) );
    }
  }

  // print summary statistics
  std::cout << "\n  *SENSOR SIMULATOR SUMMARY* \n";
  std::cout << "\t" << numFailed << " sensors failed\n";
  std::cout << "\t" << numSensors << " total sensors\n";
  std::cout << "\t" << ( (double)numFailed / (double)numSensors) * 100.0 << "% failure rate\n";
  printf("\t%.3f total time [sec]\n", time );
  printf("\t%.3f failed per sec\n\n", (double)numFailed / time );

  return 0;
}