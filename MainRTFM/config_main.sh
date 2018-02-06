#!/bin/bash

BASEDIR=".."
SENSDIR="$BASEDIR/Sensors"
LCMFILE="$SENSDIR/sensor_data.lcm"
MAINDIR="$BASEDIR/MainRTFM"

rm -rf $BASEDIR/Output
echo "(attempted to delete old Output/ in base directory)"
mkdir -p $BASEDIR/Output

cd $MAINDIR
lcm-gen -p $LCMFILE
