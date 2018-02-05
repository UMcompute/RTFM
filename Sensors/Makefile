SimSensors.ex: SensorEvent.o Sensor.o SimSensors.o
	g++ -g -Wall -O3 SensorEvent.o Sensor.o SimSensors.o -o SimSensors.ex -llcm -std=c++11

SimSensors.o: SimSensors.cpp Sensor.o SensorEvent.o
	g++ -g -Wall -c SimSensors.cpp -o SimSensors.o -llcm -std=c++11

Sensor.o: Sensor.cpp Sensor.h
	g++ -g -Wall -c Sensor.cpp -o Sensor.o -std=c++11

SensorEvent.o: SensorEvent.cpp SensorEvent.h
	g++ -g -Wall -c SensorEvent.cpp -o SensorEvent.o -std=c++11

clean:
	rm -rf *.ex *.o *~ ./sensor/
