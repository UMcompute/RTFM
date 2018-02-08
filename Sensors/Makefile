# This Makefile was tested with GNU Make
CXX=g++

# Compiler flags
CFLAGS=-g -Wall -O3
LDFLAGS=-llcm -std=c++11

SensorSim.ex: SensorEvent.o Sensor.o main_sens.o
	$(CXX) $(CFLAGS) SensorEvent.o Sensor.o main_sens.o -o SensorSim.ex $(LDFLAGS)

main_sens.o: main_sens.cpp Sensor.o SensorEvent.o
	$(CXX) $(CFLAGS) -c main_sens.cpp -o main_sens.o $(LDFLAGS)

Sensor.o: Sensor.cpp Sensor.h
	$(CXX) $(CFLAGS) -c Sensor.cpp -o Sensor.o $(LDFLAGS)

SensorEvent.o: SensorEvent.cpp SensorEvent.h
	$(CXX) $(CFLAGS) -c SensorEvent.cpp -o SensorEvent.o $(LDFLAGS)

clean:
	rm -rf *.ex *.o *~ ./sensor/
