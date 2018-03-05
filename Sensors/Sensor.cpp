#include <stdio.h>
#include "Sensor.h"

#include <math.h>
#include <fstream>
#include "sensor/sensor_data.hpp"

Sensor::Sensor()
{
  // ==========================================
  // Do not change values of DIM or NDATA
  //   without changing the LCM data struct.
  DIM = 3;
  NDATA = 6;
  // ==========================================

  active = true;
  position = new double [DIM];
  data = new double [NDATA];
  units = new double [NDATA];

  for (int i = 0; i < DIM; i++)
  {
    position[i] = 0.0;
  }
  for (int j = 0; j < NDATA; j++)
  {
    data[j] = 0.0;
  }

  // When using FDS data, we must convert the units 
  //   of the species concentrations:
  units[0] = 1.0;             // temp (degC  -->  degC)
  units[1] = 100.0;           // O2   (fraction  -->  percentage)
  units[2] = pow(10.0, 6);    // CO   (fraction  -->  ppm)
  units[3] = 100.0;           // CO2  (fraction  -->  percentage)
  units[4] = pow(10.0, 6);    // HCN  (fraction  -->  ppm)
  units[5] = 1.0;             // flux (kW/m^2  -->  kW/m^2)
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
  if (index >= 0 && index < NDATA)
  {
    data[index] = value;
  }
  else
  {
    printf("\n***error in Sensor::setData(index, value): index %d is out of bounds\n", index);
  }  
}
    
double Sensor::getData(int index)
{
  if (index >= 0 && index < NDATA)
  {
    return data[index];
  }
  else
  {
    printf("\n***error in Sensor::getData(index): index %d is out of bounds [%d] \n", index, NDATA);
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
  
// Print the data array owned by sensorArray[i].
void Sensor::printData(double time) const
{
  printf("\n\tCurrent data array held by sensor #%d at %.2f:\n\t", ID, time);
  for (int j = 0; j < NDATA; j++)
  {
    printf("%f\t", data[j]);
  }
  printf("\n");
}

// This function provides a way to simulate the 
// collection of new data at the scene of the sensor
// by reading from a file with, say, output generated
// by a fire simulation in FDS.
void Sensor::recordNewData(std::ifstream& inFile)
{
  // testing: fill all data values with a constant (1.0)
  bool testing = false;
  if (testing)
  {
    for (int i = 0; i < NDATA; i++)
    {
      this->setData(i, 1.0);
    }
  }
  // normal: get new sensor data from a file
  else
  {
    // read numerical data from FDS translated file
    std::string readVal;
    std::string::size_type sz;
    double doubleVal; 
    for (int i = 0; i < NDATA-1; i++)
    {
      if (getline(inFile, readVal, ','))
      {
        doubleVal = std::stod(readVal, &sz);
        this->setData(i, doubleVal * units[i]);
      }
      else
      {
        printf("***error: end of data file for sensor #%d\n", ID);
        this->setData(i, 0.0);
      }
    }
    if (getline(inFile, readVal, '\n'))
    {
      doubleVal = std::stod(readVal, &sz);
      this->setData(NDATA-1, doubleVal * units[NDATA-1]);
    }
    else
    {
      printf("***error: end of data file for sensor #%d\n", ID);
      this->setData(NDATA-1, 0.0);
    }
  }
}

// This function fills the LCM data struct defined in 
//  on our "sensor_data.lcm" file. Any changes in 
//  this .lcm file must be handled explicitly here 
//  in this member function and any others that use it. 
void Sensor::fillDataContainer(
  double time, 
  sensor::sensor_data& container)
{
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
