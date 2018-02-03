#!/bin/bash

# BASEDIR="/home/pbeata/Work/Michigan/fire_ideas"

# EDMDIR="$BASEDIR/EventDetection"
# COMMDIR="$BASEDIR/Communication"
# #LCMFILE="data_to_edm.lcm"
# LCMFILE="sim_sensor.lcm"

# cd $EDMDIR
# LCMPATH="$COMMDIR/$LCMFILE"
# lcm-gen -x $LCMPATH

lcm-gen -x ../Sensors/sensor_data.lcm
make -f Makefile
