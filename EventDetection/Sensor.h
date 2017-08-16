#ifndef SENSOR_H_INCLUDED
#define SENSOR_H_INCLUDED

#define NUM_DATA 7

// Sensor class to store data on per room basis
class Sensor
{
  private:
    int roomID;
    double sensorData[NUM_DATA];
    
    int itime;
    int itemp;
    int iO2;
    int iCO;
    int iCO2;
    int iHCN;
    int iflux;

    double lastTime;
    double lastTemp;
    double sumFEDheat1;
    double sumFEDheat2;
    double sumFEDsmoke;
    int fireStatus;
    
  public:
    Sensor();
    ~Sensor();
    void setID(int myID);
    void setData(int index, double newData);
    void updateTime();
    int checkFlashover();
    int checkSmokeTox();
    int checkBurnThreat();      // replaced by checkFireStatus()
    int checkFireSpread();      // replaced by checkFireStatus()
    int checkFireStatus();
    double getFEDvals(int id);
};

#endif // SENSOR_H_INCLUDED