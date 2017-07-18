/* 
  
  07-18-17 by Paul A. Beata
  takes data files and produces small data packages for each step

    $ lcm-gen -x sensor.lcm
    $ g++ MultiSensor.cpp -fopenmp -llcm
    $ export OMP_NUM_THREADS=4   # or 1, 2, 8, 16, etc..
    $ ./a.out

*/

// standard include directives
#include <iostream>
#include <omp.h>

// LCM include directives
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// main sensor program
int main(int argc, char* argv[])
{

  // input values
  // (none)

  // ================================================================

  // initialize variables
  int pid;

  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }

  // simple parallel loop to test 
  #pragma omp parallel private(pid)
  {
    pid = omp_get_thread_num();
    //std::cout << "  This is process #" << pid << "\n";
    sensor::sensor_data my_data;
    my_data.sendTime = pid * 10.0;
    printf("object %d time = %f \n", pid, my_data.sendTime);
  }

  return 0;
}
