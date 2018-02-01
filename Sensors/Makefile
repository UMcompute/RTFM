SimSensors.ex: SensorEvent.o SimSensors.o
	g++ SensorEvent.o SimSensors.o -o SimSensors.ex -llcm -std=c++11

SimSensors.o: SimSensors.cpp
	g++ -c SimSensors.cpp -o SimSensors.o -llcm -std=c++11

SensorEvent.o: SensorEvent.cpp SensorEvent.h
	g++ -c SensorEvent.cpp -o SensorEvent.o

clean:
	rm -rf *.ex *.o *~