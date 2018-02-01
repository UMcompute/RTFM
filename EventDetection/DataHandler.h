#ifndef DATAHANDLER_H_INCLUDED
#define DATAHANDLER_H_INCLUDED

#include <lcm/lcm-cpp.hpp>
#include "sensor/sensor_data.hpp"

// LCM-based class for receiving new message data
class DataHandler
{
  private:
    const int     DIM = 3;
    const int     NDATA = 6;
    int           sensorID;
    double        sendTime;
    bool          sensorStatus;

    // We assume that a sensor is placed in 3D space,
    // such that position[i] for i = 0, 1, 2 will
    // correspond to x, y, z Cartesian coordinates.
    double        *position;

    // We assume that the sensors can collect exactly
    // SIX measurements at any given time:
    //    **NDATA = 6**
    //    0 : T upper layer gas temperature
    //    1 : Q" heat flux
    //    2 : O2 oxygen
    //    3 : CO carbon monoxide
    //    4 : CO2 carbon dioxide
    //    5 : HCN hydrogen cyanide
    double        *data;

  public:
    ~DataHandler();
    DataHandler();

    void handleMessage(const lcm::ReceiveBuffer* rbuf,
           const std::string& chan,
           const sensor::sensor_data* msg);

    int getID();
    double getTime();
    bool getStatus();

    int checkSmokeTox();
    int checkBurnThreat();
    int checkFireStatus();
};

#endif // DATAHANDLER_H_INCLUDED