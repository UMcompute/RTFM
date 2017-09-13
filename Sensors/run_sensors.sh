#!/bin/bash

BASEDIR="/home/pbeata/Desktop/fire_ideas"

SENSDIR="$BASEDIR/Sensors"
COMMDIR="$BASEDIR/Communication"
LCMFILE="sim_sensor.lcm"

cd $SENSDIR
LCMPATH="$COMMDIR/$LCMFILE"
lcm-gen -x $LCMPATH

export OMP_NUM_THREADS=128
g++ -O3 $SENSDIR/MultiSensor.cpp -o $SENSDIR/MultiSensor.exe -fopenmp -llcm -std=c++11

$SENSDIR/MultiSensor.exe
