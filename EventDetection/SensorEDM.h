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
    //  (NDATA is 6 for the size of the "data" array in DataHandler)
    const int itemp = 0;
    const int iO2   = 1;
    const int iCO   = 2;
    const int iCO2  = 3;
    const int iHCN  = 4;
    const int iflux = 5;

    // SMOKE TOXICITY
    double sumFEDsmoke;
    int smokeStatus;
    const int maxSmoke = 2;
    double O2_limit = 10.0;           // percentage
    const double FED_limit = 1.0;     // FED sums to 1.0

    // BURN THREATS
    const int maxBurn = 3;
    double sumFEDheat[3] = {0.0, 0.0, 0.0};

    // FIRE STATUS
    // From (Wills 2015), 50 deg C is the limit for 
    // requiring a breathing apparatus. We use 0.5 kW/m^2
    // to help filter out traveling smoke (this helps
    // to localize the sensing to the current room). 
    // 250 deg C causes damage to PPE
    // 500 deg C + 15 kW/m^2 indicates flashover
    int fireStatus;
    const int maxFire = 3;
    const double tempLimits[3] = {50.0, 250.0, 500.0};
    const double fluxLimits[3] = { 0.0,   0.0,  15.0};
 
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
    int handleDamagedSensor(int flag);
};

#endif // SENSOREDM_H_INCLUDED
