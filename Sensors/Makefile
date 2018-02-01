SimSensors.ex: SensorEvent.o Sensor.o SimSensors.o
	g++ -O3 SensorEvent.o Sensor.o SimSensors.o -o SimSensors.ex -llcm -std=c++11

SimSensors.o: SimSensors.cpp
	g++ -c SimSensors.cpp -o SimSensors.o -llcm -std=c++11

Sensor.o: Sensor.cpp Sensor.h
	g++ -c Sensor.cpp -o Sensor.o

SensorEvent.o: SensorEvent.cpp SensorEvent.h
	g++ -c SensorEvent.cpp -o SensorEvent.o

clean:
	rm -rf *.ex *.o *~ ./sensor/
