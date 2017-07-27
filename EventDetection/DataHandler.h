#ifndef DATAHANDLER_H_INCLUDED
#define DATAHANDLER_H_INCLUDED

#define NUM_ROOMS 4

#include <lcm/lcm-cpp.hpp>
#include "send_to_edm/data_to_edm.hpp"

// LCM class for receiving message data
class DataHandler
{

  private:
    int my_num_rooms;
    double my_time_stamp;
    double my_temperature[NUM_ROOMS];
    double my_O2_conc[NUM_ROOMS];
    double my_CO_conc[NUM_ROOMS];
    double my_CO2_conc[NUM_ROOMS];
    double my_HCN_conc[NUM_ROOMS];
    double my_heat_flux[NUM_ROOMS];

  public:
    ~DataHandler();

    void handleMessage(const lcm::ReceiveBuffer* rbuf,
           const std::string& chan,
           const send_to_edm::data_to_edm* msg);
  
    // get functions to return value at provided room index
    double getTime();
    double getTemp(int index);
    double getO2(int index);
    double getCO(int index);
    double getCO2(int index);
    double getHCN(int index);
    double getFlux(int index);
};

#endif // DATAHANDLER_H_INCLUDED