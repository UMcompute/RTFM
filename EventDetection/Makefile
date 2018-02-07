EDM.ex: DataHandler.o SensorEDM.o main_edm.o
	g++ -g -Wall -O3 DataHandler.o SensorEDM.o main_edm.o -o EDM.ex -llcm -std=c++11

main_edm.o: main_edm.cpp SensorEDM.o DataHandler.o
	g++ -g -Wall -c main_edm.cpp -o main_edm.o -llcm -std=c++11

SensorEDM.o: SensorEDM.cpp SensorEDM.h DataHandler.o
	g++ -g -Wall -c SensorEDM.cpp -o SensorEDM.o -llcm -std=c++11

DataHandler.o: DataHandler.cpp DataHandler.h
	g++ -g -Wall -c DataHandler.cpp -o DataHandler.o -llcm -std=c++11

clean:
	rm -rf MainEDM.ex *.o *~ ./sensor/
