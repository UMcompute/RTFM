#!/bin/bash

sensors='4 8 16 32 64 128 256 512'
BASEDIR=".."

DATADIR="$BASEDIR/Data"
SENSDIR="$BASEDIR/Sensors"
EDMDIR="$BASEDIR/EventDetection"
MAINDIR="$BASEDIR/MainRTFM"
TESTDIR="$BASEDIR/Testing"
EXECDIR="$BASEDIR/Exec"
OUTDIR="$BASEDIR/Output"
ORIGINP="input.txt"


# configure the sensors and event detection model
$SENSDIR/config_sens.sh
$EDMDIR/config_edm.sh

# copy the original input file to Testing dir only one time
mv $EXECDIR/$ORIGINP $TESTDIR/$ORIGINP.orig

# loop over all sensor cases
for n in $sensors
do
  # create a new input file
  echo $n
  cp $TESTDIR/$ORIGINP.orig $ORIGINP
  sed -i "1s/.*/$n/" $ORIGINP
  mv $ORIGINP $EXECDIR/$ORIGINP

  # erase the data files
  rm -rf $DATADIR/file*

  # generate all the data files using new input file
  python $DATADIR/read_devc.py

  # configure and run main RTFM program
  $MAINDIR/config_main.sh
  python $MAINDIR/main_rtfm.py 1 1 0

  # copy the output data to testing dir
  OUTN="$TESTDIR/out-$n"
  mkdir $OUTN
  mv $OUTDIR/* $OUTN/
done

# return the original input file back to Exec
mv $TESTDIR/$ORIGINP.orig $EXECDIR/$ORIGINP
