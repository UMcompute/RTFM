#!/bin/bash

lcm-gen -p ../Communication/sim_sensor.lcm

lcm-gen -p ../Communication/data_to_edm.lcm
lcm-gen -p ../Communication/data_to_ifm.lcm

lcm-gen -p ../Communication/data_from_edm.lcm
lcm-gen -p ../Communication/data_from_ifm.lcm

python main_rtfm.py

rm room*
