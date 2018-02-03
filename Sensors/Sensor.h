#ifndef SENSOR_H_INCLUDED
#define SENSOR_H_INCLUDED

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

  public:
    Sensor();
    ~Sensor();
    
    int getNDATA() const;
    void setID(int inID);
    void setData(int index, double value);
    double getData(int index);
    void setActive(bool newStatus);
    bool getActive() const;
    
    void fillDataContainer(
      double time, 
      sensor::sensor_data &container);
};

#endif  // SENSOR_H_INCLUDED