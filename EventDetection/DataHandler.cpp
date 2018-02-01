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

int DataHandler::getID()
{
  return sensorID;
}

double DataHandler::getTime()            
{   
  return sendTime;
}

bool DataHandler::getStatus()
{
  return sensorStatus;
}

// SMOKE TOXICITY
int DataHandler::checkSmokeTox()
{
  return 0;
}

// BURN THREATS
int DataHandler::checkBurnThreat()
{
  return 0;
}

// FIRE STATUS
int DataHandler::checkFireStatus()
{
  return 0;
}
