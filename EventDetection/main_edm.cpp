// typical C++ directives
#include <stdio.h>
#include <fstream>

// directives needed for LCM
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// new classes
#include "DataHandler.h"
#include "SensorEDM.h"


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


// MAIN EVENT DETECTION MODEL
int main(int argc, char** argv) 
{
  // INPUT ============================
  int numSensors;
  double tmax;
  // get input file from command line argument
  std::ifstream inFile;
  std::string inFileName;
  if (argc != 2)
  {
    printf("***Error: only supply one command line argument\n");
    printf("   Expected usage:  $ ./MainEDM.ex <input_file>\n");
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
  inFile.close();  
  int writeLog = 1;
  // ==================================

  // initiate LCM and check if it is working
  printf("\n\t{Started Event Detection Model}\n");
  lcm::LCM lcm;
  if(!lcm.good()) return 1;

  // construct a Handler and subsribe to receive messages from main RTFM
  DataHandler currentData;
  lcm.subscribe("EDM_CHANNEL", &DataHandler::handleMessage, &currentData);

  // construct an array of warnings for hazard detection checks
  int *burnThreat;
  burnThreat = new int [numSensors];
  int *smokeToxicity;
  smokeToxicity = new int [numSensors];
  int *fireStatus;
  fireStatus = new int [numSensors];

  // create an array of SensorEDM class objects to store data over time
  SensorEDM *sensorArray;
  sensorArray = new SensorEDM [numSensors];
  for (int i = 0; i < numSensors; i++)
  {
    sensorArray[i].setID(i);
  }

  // preparation for output
  std::ofstream *outFiles;
  outFiles = new std::ofstream [numSensors];
  std::string file_prefix = "SensorLog-";
  std::string file_suffix = ".csv";
  std::string file_name;
  if (writeLog == 1)
  {
    for (int i = 0; i < numSensors; i++)
    {
      file_name = file_prefix + std::to_string(i) + file_suffix;
      outFiles[i].open(file_name.c_str(), std::ios::out);
    }
  }


  //-------------------------------------------------------
  // main time loop
  int sid;
  double currentTime = 0.0;
  bool active = true;
  while (currentTime < tmax)
  {
    if ( checkForNewMsg(lcm) )
    {
      // if true, a new message has been sent via LCM
      lcm.handle();

      // get the current time and the sensorID
      sid = currentData.getID();
      currentTime = currentData.getTime();
      active = currentData.getStatus();

      // assess the hazards
      if (currentTime < tmax)
      {
        // healthy sensor:
        if (active)
        {
          // FIRE STATUS
          fireStatus[sid] = sensorArray[sid].checkFireStatus(currentData);
          
          // BURN THREATS
          burnThreat[sid] = sensorArray[sid].checkBurnThreat(currentData);

          // SMOKE TOXICITY
          smokeToxicity[sid] = sensorArray[sid].checkSmokeTox(currentData);
        }
        // special case of damaged sensor:
        else
        {

        }

        // write output to propoer log file
        if (writeLog == 1)
        {
          sensorArray[sid].writeOutput(
            outFiles[sid], 
            currentData,
            smokeToxicity[sid],
            burnThreat[sid],
            fireStatus[sid]);
        }
      }
    }
  }  // end main time loop
  //-------------------------------------------------------


  // close the output files
  if (writeLog == 1)
  {
    for (int i = 0; i < numSensors; i++)
    {
      outFiles[i].close();
    }
  }

  // release dynamic memory
  delete [] outFiles;
  delete [] sensorArray;
  delete [] burnThreat;
  delete [] smokeToxicity;
  delete [] fireStatus;

  // end the event detection program
  printf("\n\n\t{End of Event Detection Model}\n");
  return 0;
}
