#!/bin/bash

lcm-gen -p ../sensor_data.lcm

# lcm-gen -p ../Communication/data_to_edm.lcm
# lcm-gen -p ../Communication/data_to_ifm.lcm

# lcm-gen -p ../Communication/data_from_edm.lcm
# lcm-gen -p ../Communication/data_from_ifm.lcm

python test_main.py

#rm room*
