#!/bin/bash

rm *.o

make -f Makefile-1

./hello

rm *.o

make -f Makefile-2

./hello

python test.py

echo -e "finished the script! \n"
