#ifndef SENSOREDM_H_INCLUDED
#define SENSOREDM_H_INCLUDED

#include "DataHandler.h"


// This class stores new data on a per-sensor basis.
class SensorEDM
{
  private:
    int sensorID;

    // set the mapping to data array
    const int itemp = 0;
    const int iflux = 1;

    const int maxWarning = 2;

    int fireStatus;
    const double tempLimits[2] = {57.0, 500.0};
    const double fluxLimits[2] = {0.6, 15.0};
    

  // define mapping from sensorData array to physical values
  // itemp   = 0;
  // iflux   = 1;
  // iO2     = 2;
  // iCO     = 3;
  // iCO2    = 4;
  // iHCN    = 5;


    /*
    double sensorData[NUM_DATA];
    

    int iO2;
    int iCO;
    int iCO2;
    int iHCN;

    double lastTime;
    double lastTemp;
    double sumFEDheat1;
    double sumFEDheat2;
    double sumFEDsmoke;
    
    */
    
  public:
    SensorEDM();
    ~SensorEDM();
    void setID(int myID);

    int checkFireStatus(DataHandler& inData);
    //int checkBurnThreat(DataHandler& inData);

    /*
    void setData(int index, double newData);
    void updateTime();
    int checkSmokeTox();
    double getFEDvals(int id);
    */
};

#endif // SENSOREDM_H_INCLUDED