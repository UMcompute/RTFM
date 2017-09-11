#!/bin/bash

BASEDIR="/home/pbeata/Desktop/fire_ideas"

EDMDIR="$BASEDIR/EventDetection"
COMMDIR="$BASEDIR/Communication"
#LCMFILE="data_to_edm.lcm"
LCMFILE="sim_sensor.lcm"

cd $EDMDIR
LCMPATH="$COMMDIR/$LCMFILE"
lcm-gen -x $LCMPATH

make clean
make -f Makefile
./main_edm.exe
