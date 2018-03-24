#!/bin/bash


# directory management
BASEDIR=".."
DATADIR="$BASEDIR/Data"
SENSDIR="$BASEDIR/Sensors"
EDMDIR="$BASEDIR/EventDetection"
MAINDIR="$BASEDIR/MainRTFM"


# we used three FDS data files for our tests:
# (uncomment the case you want to run)
# CASE 1
DEVCFILE="propane_two_fire_devc.csv"
# CASE 2
#DEVCFILE="propane_two_fire_90sec_devc.csv"
# CASE 3
#DEVCFILE="propane_two_fire_2xHRR_devc.csv"


# =========================================================
# remove current formatted data files (one for each sensor)
rm -rf $DATADIR/file*
# write new data files from FDS output (from devc file)
python $DATADIR/read_devc.py $DATADIR/$DEVCFILE
# configure the simulated sensor sub-model (runs Makefile)
$SENSDIR/config_sens.sh
# configure the event-detection model (runs Makefile)
$EDMDIR/config_edm.sh
# configure the main RTFM program (our "hub" program)
$MAINDIR/config_main.sh
# =========================================================
