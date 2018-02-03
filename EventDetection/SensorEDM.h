#ifndef SENSOREDM_H_INCLUDED
#define SENSOREDM_H_INCLUDED

#include <fstream>
#include "DataHandler.h"


// This class stores new data on a per-sensor basis.
class SensorEDM
{
  private:
    // unique ID number for sensor
    int sensorID;
    double dt;
    double lastTime;

    // set the mapping to data array
    // (NDATA is 6 for the "data" array in DataHandler)
    const int itemp = 0;
    const int iflux = 1;
    const int iO2   = 2;
    const int iCO   = 3;
    const int iCO2  = 4;
    const int iHCN  = 5;

    // SMOKE TOXICITY
    double O2_limit = 7.0;            // [%] (Alarie 2002)
    const double FED_limit = 1.0;     // FED sums to 1.0
    double sumFEDsmoke;

    // BURN THREATS
    double sumFEDheat1;
    double sumFEDheat2;

    // FIRE STATUS
    int fireStatus;
    const int maxWarning = 2;
    const double tempLimits[2] = {57.0, 500.0};
    const double fluxLimits[2] = {0.6, 15.0};
    
  public:
    SensorEDM();
    ~SensorEDM();

    // utilities
    void setID(int myID);
    void writeOutput(
        std::ofstream& fileHandle,
        DataHandler &inData,
        int smoke,
        int burn,
        int fire);
    void updateTime(double time);

    // HAZARDS
    int checkFireStatus(DataHandler& inData);
    int checkBurnThreat(DataHandler& inData);
    int checkSmokeTox(DataHandler& inData);
};

#endif // SENSOREDM_H_INCLUDED
