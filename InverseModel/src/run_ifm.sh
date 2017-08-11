#!/bin/bash
lcm-gen -p ../../Communication/data_to_ifm.lcm
lcm-gen -p ../../Communication/data_from_ifm.lcm
python main_ifm.py
rm *.pyc