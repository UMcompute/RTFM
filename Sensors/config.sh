#!/bin/bash

BASEDIR="/home/pbeata/Desktop/RTFM"
SENSDIR="$BASEDIR/Sensors"

MAIN="SimSensors"
LCMFILE="sensor_data.lcm"

cd $SENSDIR
lcm-gen -x $SENSDIR/$LCMFILE
g++ -g -Wall -O3 $SENSDIR/$MAIN.cpp -o $SENSDIR/$MAIN.ex -llcm -std=c++11
