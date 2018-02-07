SensorSim.ex: SensorEvent.o Sensor.o main_sens.o
	g++ -g -Wall -O3 SensorEvent.o Sensor.o main_sens.o -o SensorSim.ex -llcm -std=c++11

main_sens.o: main_sens.cpp Sensor.o SensorEvent.o
	g++ -g -Wall -c main_sens.cpp -o main_sens.o -llcm -std=c++11

Sensor.o: Sensor.cpp Sensor.h
	g++ -g -Wall -c Sensor.cpp -o Sensor.o -std=c++11

SensorEvent.o: SensorEvent.cpp SensorEvent.h
	g++ -g -Wall -c SensorEvent.cpp -o SensorEvent.o -std=c++11

clean:
	rm -rf *.ex *.o *~ ./sensor/
