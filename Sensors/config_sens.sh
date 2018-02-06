#!/bin/bash

BASEDIR=".."
SENSDIR="$BASEDIR/Sensors"
LCMFILE="$SENSDIR/sensor_data.lcm"

cd $SENSDIR
lcm-gen -x $LCMFILE
make
