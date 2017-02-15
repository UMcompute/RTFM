#!/bin/bash

g++ EDM_main.cpp -o EDM_main.exe -llcm -std=c++11
g++ ./fromSensors/SimpleSensor.cpp -o ./fromSensors/sensor.exe -llcm -std=c++11

