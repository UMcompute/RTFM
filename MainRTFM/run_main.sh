#!/bin/bash
rm -rf ../Output
echo "(attempted to delete old Output in base directory)"
mkdir -p ../Output
lcm-gen -p ../Sensors/sensor_data.lcm
python main_rtfm.py
