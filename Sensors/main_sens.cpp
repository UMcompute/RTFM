// C++ directives
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
#include <queue>
#include <vector>
#include <string>
#include <stdio.h>
#include <fstream>

// microsecond timer
#include <sys/time.h>
#include <chrono>
#include <stdint.h>
#include <inttypes.h>
#include <iomanip>

// LCM header files
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// user-defined classes
#include "SensorEvent.h"
#include "Sensor.h"


// This overloaded operator is needed for the priority queue 
// to sort events by ascending time stamp.
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


// A unit test using data from SFPE Handbook (defined below main)
void runUnitTest(lcm::LCM& lcmHandle, const int numSensors);


// Function to record time with microsecond accuracy
void timer(std::ofstream& timerFile);


//===================================================================
// MAIN SENSOR SIMULATOR PROGRAM
int main(int argc, char* argv[])
{

  // check if LCM is working
  printf("\n\t{Started Sensor Simulator}\n");
  lcm::LCM lcm;
  if(!lcm.good()) return 1;

  // INPUT ================================================
  int numSensors, unitTest;
  double tmax, tnom, sleepScale, failureProb;
  // get input file from command line argument
  std::ifstream inFile;
  std::string inFileName;
  if (argc != 2)
  {
    printf("***Error: please provide exactly one command line argument\n");
    printf("   Expected usage:  $ ./SimSensors.ex [input_file.txt]\n");
    return 1;
  }
  else
  {
    inFileName = argv[1];
    printf("\n%s has input file: %s \n\n", argv[0], inFileName.c_str());
  }
  // read the four input values needed
  inFile.open(inFileName.c_str());
  inFile >> numSensors;
  inFile >> tmax;
  inFile >> tnom;
  inFile >> failureProb;
  inFile >> sleepScale;
  inFile >> unitTest;
  inFile.close();
// ======================================================  

  // fixed input for file management
  std::string channelPrefix = "SENSOR";
  std::string filePrefix = "../Data/file";
  std::string fileSuffix = ".csv";
  std::string timerOutput = "../Output/send_time.csv";

  // initialize the sensor simulator variables  
  srand(100);
  int sid; 
  int numFailed = 0;
  double sleepConversion = sleepScale * pow(10.0, 6.0);
  double time = 0.0;
  double dtMin = 0.5;
  double dt, st, myTime, failCheck;

  // initialize the LCM data structures
  std::string channel;
  sensor::sensor_data dataToSend;
  Sensor *sensorArray;
  sensorArray = new Sensor [numSensors];

  // data file management
  std::string dataFile;
  std::ifstream *fileList;
  fileList = new std::ifstream [numSensors];
  std::ofstream timerFile;

  // declare the priority queue for holding "sensorEvent" events
  std::priority_queue< SensorEvent, std::vector<SensorEvent>, std::greater<SensorEvent> > eventQueue;

  // Initialize the queue with the first data measurement events
  //  for each sensor (for the normal sensor simulation) ...
  if (unitTest == 0)
  {
    for (int i = 0; i < numSensors; i++)
    {
      // add initial event to the queue for each sensor
      myTime = getRandDble() * tnom;
      eventQueue.push( SensorEvent(i, myTime) );

      // open files to read sensor data from:
      dataFile = filePrefix + std::to_string(i) + fileSuffix;
      fileList[i].open(dataFile.c_str());
    }
    // output file for timer
    timerFile.open(timerOutput.c_str());  
  }
  // ... or perform unit test to assess system:
  else if (unitTest == 1)
  {
    runUnitTest(lcm, numSensors);
  }
  // ... or there is an error in the runUnitTest in ../Exec/inputs.h
  else
  {
    printf("***Error: invalid value for int unitTest (must be 0 or 1)\n");
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

    // test if sensor has failed; update its data
    if ( sensorArray[sid].getActive() )
    {
      failCheck = getRandDble();
      // sensor has failed:
      if (failCheck < failureProb)
      {
        // if the sensor has failed (signifying damage), 
        //   then fill the data array with -1's
        printf("\n***sensor #%d FAILED at time = %f sec***\n", sid, time);
        sensorArray[sid].setActive(false);
        numFailed += 1;
        for (int j = 0; j < NDATA; j++)
        {
          sensorArray[sid].setData(j, -1.0);
        }
      }
      // sensor has not failed:
      else
      {
        // active sensors record new data from file
        sensorArray[sid].recordNewData(fileList[sid]);
      }
    }

    // prepare data to send to the main RTFM program
    sensorArray[sid].fillDataContainer(time, dataToSend);
    channel = channelPrefix + std::to_string(sid);

    // record the publish time
    if (sid == 0) timer(timerFile);

    // publish the data using LCM
    lcm.publish(channel, &dataToSend);

    // add a new event to the sensor queue
    dt = getRandDble() * tnom + dtMin;
    if ( (time + dt) < tmax)
    {
      eventQueue.push( SensorEvent(sid, time + dt) );
    }
  }
  //-------------------------------------------------------
 

  // send final message at time = tmax
  time = tmax;
  for (sid = 0; sid < numSensors; sid++)
  {
    // prepare data to send
    if ( sensorArray[sid].getActive() )
    {
      sensorArray[sid].recordNewData(fileList[sid]);
    }
    sensorArray[sid].fillDataContainer(time, dataToSend);
    channel = channelPrefix + std::to_string(sid);

    // record the publish time
    if (sid == 0) timer(timerFile);

    // publish the data using LCM
    lcm.publish(channel, &dataToSend);
  } 
 
  // print summary statistics
  usleep(sleepConversion);
  printf("\n\t{Sensor Simulator Summary}\n");
  printf("\t  %d sensors failed\n", numFailed);
  printf("\t  %d total sensors\n", numSensors);
  printf("\t  %.2f percent failure rate\n", ( (double)numFailed / (double)numSensors) * 100.0);
  printf("\t  %.3f total time [sec]\n", time );

  // free dynamic memory
  delete [] sensorArray;
  if (unitTest == 0)
  {
    for (int i = 0; i < numSensors; i++)
    {
      fileList[i].close();
    }
    delete [] fileList;
    timerFile.close();
  }

  // exit the main program
  return 0;
}
//===================================================================


// A unit test using data from SFPE Handbook
void runUnitTest(lcm::LCM& lcmHandle, const int numSensors)
{
  printf("\n\t{UNIT TEST USING %d SENSORS}\n\n", numSensors);
  bool verbose = true;

  // used for usleep function:
  double sleepTime = 0.2 * pow(10.0, 6.0);
  
  // data measurement mapping:
  //    0 = temp
  //    1 = flux
  //    2 = O2
  //    3 = CO
  //    4 = CO2
  //    5 = HCN  

  // N is the number of time steps in this test
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

      // send current data
      sensorArray[i].fillDataContainer(time[n], dataToSend);
      channel = channelPrefix + std::to_string(i);
      lcmHandle.publish(channel, &dataToSend);

      // print output
      if (verbose)
      {
        sensorArray[i].printData(time[n]);
        printf("\t*published message on %s*\n\n", channel.c_str() );
      }
    }
  }

  // free dynamic memory
  delete [] sensorArray;

  // exit unit test
  printf("\t{END UNIT TEST}\n");
}


// timer function
void timer(std::ofstream& timerFile)
{
  static char buffer[29];
  static int64_t usec;
  static struct tm* tm_info;
  static struct timeval tv;

  gettimeofday(&tv, NULL);
  usec = tv.tv_usec;
  if (usec >= 1000000)
  {
    usec -= 1000000;
    tv.tv_sec++;
  }
  tm_info = localtime(&tv.tv_sec);
  strftime(buffer, 29, "%H,%M,%S", tm_info);
  
  // output
  timerFile << buffer << ".";
  timerFile << std::setw(6) << std::setfill('0') << usec << "\n";
}

