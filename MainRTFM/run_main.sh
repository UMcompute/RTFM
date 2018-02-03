#!/bin/bash
mkdir -p ../Output
lcm-gen -p ../Sensors/sensor_data.lcm
python main_rtfm.py
