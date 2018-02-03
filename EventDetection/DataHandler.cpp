#include <stdio.h>
#include "DataHandler.h"
#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"


DataHandler::DataHandler()
{
  // initialize the position and data arrays with zeros
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

DataHandler::~DataHandler() 
{
  // custom destructor to delete dynamic memory
  delete [] position;
  delete [] data;
}

void DataHandler::handleMessage(const lcm::ReceiveBuffer* rbuf,
       const std::string& chan,
       const sensor::sensor_data* msg)
{
  printf("      ==>> EDM recv %.3f from sensor #%d\n", msg->sendTime, msg->sensorID);
  
  sensorID = msg->sensorID;
  sendTime = msg->sendTime;
  sensorStatus = msg->status;
  
  for (int i = 0; i < DIM; i++)
  {
    position[i] = msg->position[i];
  }

  for (int i = 0; i < NDATA; i++)
  {
    data[i] = msg->data[i];
  }

}

int DataHandler::getID() const
{
  return sensorID;
}

double DataHandler::getTime() const
{   
  return sendTime;
}

bool DataHandler::getStatus() const
{
  return sensorStatus;
}

void DataHandler::getPosition(double *x, int n)
{
  // This fucntion expects x to have dimension of n:
  //   double x[n];
  if (n != DIM)
  {
    printf("***Warning: DIM=%d does not match input n=%d in DataHandler \n", DIM, n);
  }
  if (n <= DIM)
  {    
    for (int i = 0; i < n; i++)
    {
      x[i] = position[i];
    }
  }
  else
  {
    printf("***Error: n=%d is out of bounds for DIM=%d in DataHandler \n", n, DIM); 
  }
}

double DataHandler::getDataValue(int index)
{
  // This function will check if the requested index is in bounds
  if (0 <= index && index < NDATA)
  {
    return data[index];
  }
  else
  {
    printf("***Error: tried to access index %d in DataHandler (NDATA = %d)\n", index, NDATA);
    return -1.0;
  }
}