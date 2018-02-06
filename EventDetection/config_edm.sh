#!/bin/bash

BASEDIR=".."
SENSDIR="$BASEDIR/Sensors"
LCMFILE="$SENSDIR/sensor_data.lcm"
EDMDIR="$BASEDIR/EventDetection"

cd $EDMDIR
lcm-gen -x $LCMFILE
make -f Makefile
