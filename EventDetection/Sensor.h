#ifndef SENSOR_H_INCLUDED
#define SENSOR_H_INCLUDED

#define NUM_DATA 7

// Sensor class to store data on per room basis
class Sensor
{
  private:
    int roomID;
    double sensorData[NUM_DATA];
    int itemp;
    int iflux;
    
  public:
    Sensor();
    ~Sensor();
    void setID(int myID);
    void setData(int index, double newData);
    int checkFlashover();
    int checkSmokeTox();
    int checkBurnThreat();
    int checkFireSpread();
};

#endif // SENSOR_H_INCLUDED