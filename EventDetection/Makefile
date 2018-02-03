MainEDM.ex: DataHandler.o SensorEDM.o main_edm.o
	g++ DataHandler.o SensorEDM.o main_edm.o -o MainEDM.ex -llcm -std=c++11

main_edm.o: main_edm.cpp
	g++ -c main_edm.cpp -o main_edm.o -llcm -std=c++11

SensorEDM.o: SensorEDM.cpp SensorEDM.h DataHandler.o
	g++ -c SensorEDM.cpp -o SensorEDM.o -llcm -std=c++11

DataHandler.o: DataHandler.cpp DataHandler.h
	g++ -c DataHandler.cpp -o DataHandler.o -llcm -std=c++11

clean:
	rm -rf MainEDM.ex *.o *~