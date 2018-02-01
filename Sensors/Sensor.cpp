#include <stdio.h>
#include "Sensor.h"

#include "sensor/sensor_data.hpp"

Sensor::Sensor()
{
  active = true;
  DIM = 3;
  NDATA = 6;

  position = new double [DIM];
  data = new double [NDATA];

  for (int i = 0; i < DIM; i++)
  {
    position[i] = 0.0;
  }
  for (int j = 0; j < NDATA; j++)
  {
    data[j] = 0.0;
  }
}

Sensor::~Sensor()
{
  delete [] position;
  delete [] data;
}
    
int Sensor::getNDATA() const
{
  return NDATA;
}
    
void Sensor::setID(int inID)
{
  ID = inID;
}
    
void Sensor::setData(
  int index, 
  double value)
{
  data[index] = value;
}
    
double Sensor::getData(int index) const
{
  if (index >= 0 && index < NDATA)
  {
    return data[index];
  }
  else
  {
    printf("\n***error in Sensor::getData(index): index %d is out of bounds\n", index);
    return -1.0;
  }
}
    
void Sensor::setActive(bool newStatus)
{
  active = newStatus;
}
    
bool Sensor::getActive() const
{
  return active;
}
    
void Sensor::fillDataContainer(
  double time, 
  sensor::sensor_data &container)
{
  /*
  based on our "sensor_data.lcm" data struct:
    struct sensor_data
    {
      int32_t sensorID;
      double  sendTime;
      boolean status;
      int32_t dim;
      double  position[dim];
      int32_t ndata;
      double  data[ndata];
    }
  */

  // set scalar values to be sent
  container.sensorID = ID;
  container.sendTime = time;
  container.status = active;
  container.dim = DIM;
  container.ndata = NDATA;

  // set vectors to be sent
  container.position.resize(container.dim);
  for (int i = 0; i < container.dim; i++)
  {
    container.position[i] = position[i];
  } 
  container.data.resize(container.ndata);
  for (int j = 0; j < container.ndata; j++)
  {
    container.data[j] = data[j];
  }
}