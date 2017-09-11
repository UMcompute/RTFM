#include <iostream>
#include "DataHandler.h"
#include <lcm/lcm-cpp.hpp>
//#include "send_to_edm/data_to_edm.hpp"
#include "sim_sensor/sensor_data.hpp"

DataHandler::~DataHandler() 
{
  // custom destructor
  // (if needed for deleting dynamic memory later)
}

void DataHandler::handleMessage(const lcm::ReceiveBuffer* rbuf,
       const std::string& chan,
       const sim_sensor::sensor_data* msg)
{
  std::cout << "got a message in EDM at time " << msg->sendTime << std::endl;
  roomNum     = msg->roomNum;
  sendTime    = msg->sendTime;
  temperature = msg->temperature;
  O2conc      = msg->O2conc;
  COconc      = msg->COconc;
  CO2conc     = msg->CO2conc;
  HCNconc     = msg->HCNconc;
  heatFlux    = msg->heatFlux;
}


// "getter" functions to return data values
int DataHandler::getRoom()
{
  return roomNum;
}
double DataHandler::getTime()            
{   
  return sendTime;
}
double DataHandler::getTemp()   
{   
  return temperature;
}
double DataHandler::getO2()     
{   
  return O2conc;
}
double DataHandler::getCO()     
{   
  return COconc;
}
double DataHandler::getCO2()    
{   
  return CO2conc;
}
double DataHandler::getHCN()    
{   
  return HCNconc;
}
double DataHandler::getFlux()   
{   
  return heatFlux;
}
