#!/bin/bash
lcm-gen -x ../Communication/sim_sensor.lcm
export OMP_NUM_THREADS=4
g++ MultiSensor.cpp -fopenmp -llcm -std=c++11
./a.out