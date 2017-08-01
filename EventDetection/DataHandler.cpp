#include <iostream>
#include "DataHandler.h"
#include <lcm/lcm-cpp.hpp>
#include "send_to_edm/data_to_edm.hpp"

DataHandler::~DataHandler() 
{
  // custom destructor
  // (if needed for deleting dynamic memory later)
}

void DataHandler::handleMessage(const lcm::ReceiveBuffer* rbuf,
       const std::string& chan,
       const send_to_edm::data_to_edm* msg)
{
  std::cout << "got a message in EDM at time " << msg->time_stamp << std::endl;
  // update all incoming data in local memory
  int i;
  my_num_rooms = msg->num_rooms;
  my_time_stamp = msg->time_stamp;
  for (i = 0; i < my_num_rooms; i++)
  {
    my_temperature[i] = msg->temperature[i];
    my_O2_conc[i] = msg->O2_conc[i];
    my_CO_conc[i] = msg->CO_conc[i];
    my_CO2_conc[i] = msg->CO2_conc[i];
    my_HCN_conc[i] = msg->HCN_conc[i];
    my_heat_flux[i] = msg->heat_flux[i];
  }
}

// get functions to return value at provided room index
// todo: provide error handling for reaching outside the bounds with index
double DataHandler::getTime()            
{   
  return my_time_stamp;
}
double DataHandler::getTemp(int index)   
{   
  return my_temperature[index];   
}
double DataHandler::getO2(int index)     
{   
  return my_O2_conc[index];       
}
double DataHandler::getCO(int index)     
{   
  return my_CO_conc[index];       
}
double DataHandler::getCO2(int index)    
{   
  return my_CO2_conc[index];      
}
double DataHandler::getHCN(int index)    
{   
  return my_HCN_conc[index];      
}
double DataHandler::getFlux(int index)   
{   
  return my_heat_flux[index];     
}