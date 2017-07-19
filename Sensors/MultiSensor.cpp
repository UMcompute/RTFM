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

// LCM include directives
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// main sensor program
int main(int argc, char* argv[])
{

  // input values
  double waitUsec = 1.0;

  // ================================================================

  // initialize constants and check for number of threads to match
  const int NUM_ROOMS = 4;
  const int NUM_STEPS = 4;

  // declare variables
  int i, j;
  int pid;
  int num_threads;
  double readValue;
  std::string my_file;
  std::string my_line;
  //std::ifstream if_file;

  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }
  
  /*
  // simple parallel loop to test for case threads = rooms
  #pragma omp parallel private(pid)
  {
    pid = omp_get_thread_num();
    //std::cout << "  This is process #" << pid << "\n";
    
    sensor::sensor_data my_data;
    my_data.sendTime = pid * 10.0;
    printf("object %d time = %f \n", pid, my_data.sendTime);
    
    usleep( pid * pow(10.0, 6.0) );
    my_data.sendTime = pid * 100.0;
    printf("\nobject %d time = %f \n", pid, my_data.sendTime);
    
  }

  // potentially unnecessary barrier (check this)
  #pragma omp barrier
  */

  // simple parallel test for when num_threads != num_rooms
  #pragma omp parallel private(pid)
  {
    pid = omp_get_thread_num();
    printf("this is process #%d \n", pid);

    if (pid == 0)
    {
      num_threads = omp_get_num_threads();
      printf("num_threads = %d\n", num_threads);
      if (num_threads != NUM_ROOMS)
      {
        printf("***warning: must set proper number of threads (%d) for %d rooms; use \n", num_threads, NUM_ROOMS);
        printf("$ export OMP_NUM_THREADS=%d \n", NUM_ROOMS);
      }
    }

    #pragma omp for private(i, j, my_file, my_line, readValue)
    for (i = 0; i < NUM_ROOMS; i++)
    {

      my_file = "./data/file" + std::to_string(i) + ".txt";
      printf("%s\n", my_file.c_str());
      std::ifstream if_file(my_file.c_str());

      while (getline(if_file, my_line, ','))
      {
        std::istringstream iss(my_line);
        while (iss >> readValue)
        {
          usleep( 0.5 * pow(10.0, 6.0) );
          printf("thread #%d got value %f in room #%d \n", pid, readValue, i);  
        }
      }

      if_file.close();

      /*

      sensor::sensor_data my_data;
      my_data.sendTime = pid * 10.0;

      for (j = 0; j < NUM_STEPS; j++)
      {
        usleep( pid * pow(10.0, 6.0) );

        //printf("  process #%d got room #%d with time %f [%d] \n", pid, i, my_data.sendTime, j);
      }

      */

    }

  }

  return 0;
}
