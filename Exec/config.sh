#!/bin/bash

BASEDIR=".."

DATADIR="$BASEDIR/Data"
SENSDIR="$BASEDIR/Sensors"
EDMDIR="$BASEDIR/EventDetection"
MAINDIR="$BASEDIR/MainRTFM"


python $DATADIR/read_devc.py

$SENSDIR/config_sens.sh

$EDMDIR/config_edm.sh

$MAINDIR/config_main.sh
