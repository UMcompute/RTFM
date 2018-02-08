# This Makefile was tested with GNU Make
CXX=g++

# Compiler flags
CFLAGS=-g -Wall -O3
LDFLAGS=-llcm -std=c++11

EDM.ex: DataHandler.o SensorEDM.o main_edm.o
	$(CXX) $(CFLAGS) DataHandler.o SensorEDM.o main_edm.o -o EDM.ex $(LDFLAGS)

main_edm.o: main_edm.cpp SensorEDM.o DataHandler.o
	$(CXX) $(CFLAGS) -c main_edm.cpp -o main_edm.o $(LDFLAGS) 

SensorEDM.o: SensorEDM.cpp SensorEDM.h DataHandler.o
	$(CXX) $(CFLAGS) -c SensorEDM.cpp -o SensorEDM.o $(LDFLAGS)
 
DataHandler.o: DataHandler.cpp DataHandler.h
	$(CXX) $(CFLAGS) -c DataHandler.cpp -o DataHandler.o $(LDFLAGS) 

clean:
	rm -rf *.ex *.o *~ ./sensor/
