#!/bin/bash

BASEDIR="/home/pbeata/Desktop/RTFM"
SENSDIR="$BASEDIR/Sensors"

MAIN="SimSensors"
LCMFILE="sensor_data.lcm"

cd $SENSDIR
lcm-gen -x $SENSDIR/$LCMFILE
make
