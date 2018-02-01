#!/bin/bash

BASEDIR="/home/pbeata/Work/Michigan/fire_ideas"

SENSDIR="$BASEDIR/Sensors"
# COMMDIR="$BASEDIR/Communication"
LCMFILE="../sensor_data.lcm"


cd $SENSDIR
#LCMPATH="$COMMDIR/$LCMFILE"

lcm-gen -x $LCMFILE

# export OMP_NUM_THREADS=128

g++ -g -Wall -O3 $SENSDIR/SimSensors.cpp -o $SENSDIR/SimSensors.ex -llcm -std=c++11

# $SENSDIR/MultiSensor.exe
