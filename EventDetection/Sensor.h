#ifndef SENSOR_H_INCLUDED
#define SENSOR_H_INCLUDED

#define NUM_DATA 7

// Sensor class to store data on per room basis
class Sensor
{
  private:
    int roomID;
    double sensorData[NUM_DATA];
    
  public:
    Sensor();
    ~Sensor();
    void setID(int myID);
};

#endif // SENSOR_H_INCLUDED