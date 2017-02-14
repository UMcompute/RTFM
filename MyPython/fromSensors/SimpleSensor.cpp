/* 01-11-17
   Takes completed FDS_output.dat and produces small data 
   packages update.dat for each step

   $ g++ SimpleSensor.cpp -o sensor.exe -llcm
   $ ./sensor.exe

   (make sure the FDS_output.dat file is in the same directory)
 
*/

#include <iostream>
#include <fstream>
#include <math.h>
#include <string>
#include <sstream>
#include <string>
#include <unistd.h>
#include <chrono>
#include <ctime>

#include <lcm/lcm-cpp.hpp>
#include "fromSensor/sensor.hpp"

using namespace std;

int main(int argc, char* argv[])
{

  // get input from command line
  printf("The name of this program is '%s'. \n", argv[0]);
	printf("This program was invoked with %d argument(s). \n", argc - 1);
	if (argc == 1) 
	{
	  printf("***error: expecting a data file passed from command line \n");
	  return 1;
	}
  printf("\n");
	
  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }
  fromSensor::sensor my_data;	

  // initialize the data table
  const int ROWS = 300;
  const int COLS = 3;
  double inData[ROWS][COLS];
  const int MAX_STEPS = 10;
  double waitUsec = 1.0;

  // read in line-by-line of the FDS data
  string filename = argv[1];
  ifstream file(filename.c_str());
  string line;
  double readValue;
  int i, j;
  i = 0;
  while (getline(file, line)) {
    istringstream iss(line);
    j = 0;
    while (iss >> readValue) {
      //cout << "value = " << readValue << " at (" << i << ", " << j << ")" << '\t';
      inData[i][j] = readValue;
      j++;
    }
    i++;
    //cout << endl;
  }
  file.close();

  // generate a data package for each time step
  double outData[COLS];
  for (int iTime = 0; iTime < MAX_STEPS; iTime++) 
  {
    string filename = "update";
    filename = filename + ".dat";
    ofstream myfile;
    myfile.open (filename.c_str());
    for (int jCols = 0; jCols < COLS; jCols++) 
    {
      myfile << inData[iTime][jCols] << "\t" << "\t";
      outData[jCols] = inData[iTime][jCols];
    }
    myfile << "\n";
    myfile.close();
    //cout << "finished step #" << iTime << " with t = " << inData[iTime][0] << endl;
    
    //===============================================================
    // SEND LCM MSG TO MAIN PROGRAM WITH NEW SENSOR DATA    
      // define sensor info in LCM data structure
      my_data.time = outData[0];
      my_data.flux = outData[1];
      my_data.temp = outData[2];
      // print time stamp of message send
      std::chrono::time_point<std::chrono::system_clock> end;
      end = std::chrono::system_clock::now();
      std::time_t end_time = std::chrono::system_clock::to_time_t(end);
      std::cout << "\n   SENSOR sent time " << outData[0] << " with timestamp: " << std::ctime(&end_time) <<"\n";
      // publish message for the receiver and exit
      lcm.publish("SENSOR", &my_data);
    //===============================================================  
    
    usleep( waitUsec * pow(10.0, 6.0) );
  }

  return 0;
}
