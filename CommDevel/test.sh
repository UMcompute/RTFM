#!/bin/bash

FIND_START=`grep "start" status.txt -c`
#echo $FIND_START

if [ $FIND_START = "1" ]; then
    echo "good"
else
    echo "continue to wait for signal"
fi

