/* 
  
  07-18-17 by Paul A. Beata
  takes data files and produces small data packages for each step

    $ lcm-gen -x sensor.lcm
    $ g++ MultiSensor.cpp -fopenmp -llcm -std=c++11
    $ export OMP_NUM_THREADS=4   # or 1, 2, 8, 16, etc..
    $ ./a.out

*/

// standard include directives
#include <iostream>
#include <omp.h>
#include <fstream>
#include <math.h>
#include <string>
#include <sstream>
#include <unistd.h>
#include <chrono>
#include <ctime>
#include <cstdlib>

// LCM include directives
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// main sensor program
int main(int argc, char* argv[])
{

  // initialize constants
  const int NUM_ROOMS = 4;    // number of rooms in simulation
  const int NUM_DATA = 5;     // number of columns in data files
  double nominalFreq = 1.00;  // [Hz]
  double noise = 0.05;        // [%]
  int convFact = 1000000;     // [s] to [us]
  float roundup = 0.5;        // [us]
  srand(22);                  // seed for random numbers

  // ================================================================

  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }

  // declare variables
  int num_threads = 0;
  double my_row[NUM_DATA];
  std::string file_prefix = "./data/file";
  std::string file_suffix = ".csv";
  std::string channel_pre = "ROOM";

  // sensor variables
  float period = 1.0 / nominalFreq;
  float min_per = (1.0 - noise) * period;
  float max_per = (1.0 + noise) * period;
  min_per = convFact * min_per + roundup;
  max_per = convFact * max_per + roundup; 
  int min_time = (int)min_per;
  int max_time = (int)max_per;
  int rand_range = max_time - min_time;

  // distribute one room to each thread
  #pragma omp parallel private(my_row)
  {
    // get unique thread number
    int pid = omp_get_thread_num();
    //printf("this is process #%d \n", pid);

    // check to make sure #threads = #rooms
    if (pid == 0)
    {
      num_threads = omp_get_num_threads();
      if (num_threads != NUM_ROOMS)
      {
        printf("***warning: must set proper number of threads (%d) for %d rooms; use \n", num_threads, NUM_ROOMS);
        printf("$ export OMP_NUM_THREADS=%d \n", NUM_ROOMS);
      }
    }

    // declare unique LCM data packet and channel name
    sensor::sensor_data my_data;
    std::string my_chan = channel_pre + std::to_string(pid);

    // open "my" data file
    std::string my_file;
    my_file = file_prefix + std::to_string(pid) + file_suffix;
    std::ifstream if_file(my_file.c_str());

    // read in data from file and publish to LCM network
    std::string my_line;
    int col = 0;
    double readValue;
    int rand_int;
    double rand_val;
    double my_time = 0.0;
    while (getline(if_file, my_line, ','))
    {
      std::istringstream iss(my_line);
      while (iss >> readValue)
      {
        my_row[col] = readValue;
        if (col < NUM_DATA - 1)
        {
          // continue reading on row
          col += 1;  
        }
        else
        {
          // start new row
          col = 0;

          // package the data from the file
          my_data.roomNum = pid;
          my_data.temperature = my_row[0];
          my_data.O2conc = my_row[1];
          my_data.COconc = my_row[2];
          my_data.CO2conc = my_row[3];
          my_data.heatFlux = my_row[4];

          // compute random noise for delay time
          rand_int = rand()%rand_range + min_time;
          rand_val = ((double)rand_int) / convFact;          

          // wait random time and then send
          my_time += rand_val;
          my_data.sendTime = my_time;
 
          //=====================================================
          // PUBLISH LCM MSG TO MAIN PROGRAM WITH NEW SENSOR DATA
          usleep( rand_val * pow(10.0, 6.0) );
          std::chrono::time_point<std::chrono::system_clock> tend;
          tend = std::chrono::system_clock::now();
          std::time_t end_time = std::chrono::system_clock::to_time_t(tend);
          std::cout << "SENSOR " << pid << " send time at " << std::ctime(&end_time) <<"\n";
          lcm.publish(my_chan, &my_data);
          //=====================================================
        }
        /*
        // if finished with current row of data
        if (col == NUM_DATA - 1)
        {

          // package the data from the file
          my_data.roomNum = pid;
          my_data.temperature = my_row[0];
          my_data.O2conc = my_row[1];
          my_data.COconc = my_row[2];
          my_data.CO2conc = my_row[3];
          my_data.heatFlux = my_row[4];

          std::cout << my_row[4] << "   " << my_data.heatFlux << "\n";

          // compute random noise for delay time
          rand_int = rand()%rand_range + min_time;
          rand_val = ((double)rand_int) / convFact;

          // wait random time and then send
          usleep( rand_val * pow(10.0, 6.0) );
          my_time += rand_val;
          my_data.sendTime = my_time;

          //=====================================================
          // PUBLISH LCM MSG TO MAIN PROGRAM WITH NEW SENSOR DATA
          // time stamp
          std::chrono::time_point<std::chrono::system_clock> tend;
          tend = std::chrono::system_clock::now();
          std::time_t end_time = std::chrono::system_clock::to_time_t(tend);
          std::cout << "SENSOR " << pid << " send time at " << std::ctime(&end_time) <<"\n";
          lcm.publish(my_chan, &my_data);
          //=====================================================
        }
        */
      }
    }
    // close "my" data file
    if_file.close();
  
  }   // exit parallel loop  
  
  //printf("num_threads = %d \n", num_threads);
  return 0;
}
