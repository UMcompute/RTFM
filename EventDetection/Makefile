main_edm.exe: DataHandler.o Sensor.o main_edm.o
	g++ DataHandler.o Sensor.o main_edm.o -o main_edm.exe -llcm -std=c++11

main_edm.o: main_edm.cpp
	g++ -c  main_edm.cpp -o main_edm.o -llcm -std=c++11

DataHandler.o: DataHandler.cpp DataHandler.h
	g++ -c DataHandler.cpp -o DataHandler.o -llcm -std=c++11

Sensor.o: Sensor.cpp Sensor.h
	g++ -c Sensor.cpp -o Sensor.o

clean:
	rm -rf main_edm.exe *.o *~
