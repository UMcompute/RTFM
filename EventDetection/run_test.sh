#!/bin/bash
lcm-gen -x ../Communication/data_to_edm.lcm
g++ -c Sensor.cpp -o Sensor.o
g++ -c test_edm.cpp -o test_edm.o
g++ Sensor.o test_edm.o 
./a.out