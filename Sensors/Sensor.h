#ifndef SENSOR_H_INCLUDED
#define SENSOR_H_INCLUDED

#include <fstream>
#include "sensor/sensor_data.hpp"

class Sensor
{
  private:
    int DIM;
    int NDATA;
    int ID;
    bool active;
    double *position;
    double *data;
    double *units;

  public:
    Sensor();
    ~Sensor();
    
    int getNDATA() const;
    void setID(int inID);
    void setData(int index, double value);
    double getData(int index);
    void setActive(bool newStatus);
    bool getActive() const;
    void printData(double time) const;
    void recordNewData(std::ifstream& inFile);
    void fillDataContainer(
      double time, 
      sensor::sensor_data& container);
};

#endif  // SENSOR_H_INCLUDED