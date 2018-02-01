#ifndef DATAHANDLER_H_INCLUDED
#define DATAHANDLER_H_INCLUDED

#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// LCM class for receiving message data
class DataHandler
{

  private:
    int       roomNum;
    double    sendTime;
    double    temperature;
    double    O2conc;
    double    COconc;
    double    CO2conc;
    double    HCNconc;
    double    heatFlux;

  public:
    ~DataHandler();
    void handleMessage(const lcm::ReceiveBuffer* rbuf,
           const std::string& chan,
           const sensor::sensor_data* msg);

    // "getter" functions to return most recent message data
    int getRoom();
    double getTime();
    double getTemp();
    double getO2();
    double getCO();
    double getCO2();
    double getHCN();
    double getFlux();
};

#endif // DATAHANDLER_H_INCLUDED