#include <math.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
#include <queue>
#include <vector>
#include <string>


// LCM include directives
#include <lcm/lcm-cpp.hpp>
#include "sim_sensor/sensor_data.hpp"


#define DIM 3
#define NDATA 6


class SensorEvent
{
  public:
    SensorEvent(int inID, double inTime)
    {
      ID = inID;
      time = inTime;
    }
    int getID() const
    {
      return ID;
    }
    double getTime() const
    {
      return time; 
    }
  private:
    int ID;
    double time;
};


class Sensor
{
  public:
    Sensor()
    {
      active = true;
      for (int i = 0; i < DIM; i++)
      {
        position[i] = 0.0;
      }
      for (int j = 0; j < NDATA; j++)
      {
        data[j] = 0.0;
      }
    }
    void setID(int inID)
    {
      ID = inID;
    }
    void setData(int index, double value)
    {
      data[index] = value;
    }
    double getData(int index)
    {
      if (index >= 0 && index < NDATA)
      {
        return data[index];
      }
      else
      {
        std::cout << "***error in getData(index): index out of bounds\n";
        return 10000.0;
      }
    }
    void setActive(bool newStatus)
    {
      active = newStatus;
    }
    bool getActive()
    {
      return active;
    }
    void fillDataContainer(
      double time, 
      sim_sensor::sensor_data &container)
    {

      /*
      based on our "sim_sensor.lcm" data struct: 

        struct sensor_data
        {
          int32_t sensorID;
          double  sendTime;
          boolean status;
          int32_t dim;
          double  position[dim];
          int32_t ndata;
          double  data[ndata];
        }

      */

      // set scalar values to be sent
      container.sensorID = ID;
      container.sendTime = time;
      container.status = active;
      container.dim = DIM;
      container.ndata = NDATA;

      // set vectors to be sent
      container.position.resize(container.dim);
      for (int i = 0; i < container.dim; i++)
      {
        container.position[i] = position[i];
      } 
      container.data.resize(container.ndata);
      for (int j = 0; j < container.ndata; j++)
      {
        container.data[j] = data[j];
      }

    }
  private:
    int ID;
    bool active;
    double position[DIM];
    double data[NDATA];
};


bool operator>(const SensorEvent& lhs, const SensorEvent& rhs)
{
  return (lhs.getTime() > rhs.getTime());
}


// returns a random number between 0 and 1
double getRandDble()
{
  double p = 0.0;
  p = ((double)((rand() % 1000000) / 1000000.0));
  return p;
}


int main(int argc, char* argv[])
{

  // INPUT ============================
  // (move this into an input file?)
  const int numSensors = 4;
  const double tnom = 2.5;
  const double tmax = 11.0;
  const double failureProb = 0.40;
  // ==================================

  srand(1000);
  int sid; 
  int numFailed = 0;
  double sleepConversion = pow(10.0, 6.0);
  double time = 0.0;
  double dt, st, myTime, failCheck;

  sim_sensor::sensor_data dataToSend;
  Sensor sensorArray[numSensors];
  std::string channelPrefix = "SENSOR";
  std::string channel;

  // declare the primary queue for sensorEvent events
  std::priority_queue< SensorEvent, std::vector<SensorEvent>, std::greater<SensorEvent> > eventQueue;

  // check if LCM is working
  lcm::LCM lcm;
  if(!lcm.good())
  {
    return 1;
  }

  // initialize the queue and sensor array
  for (int i = 0; i < numSensors; i++)
  {
    myTime = getRandDble() * tnom;
    eventQueue.push( SensorEvent(i, myTime) );
    sensorArray[i].setID(i);
  }

  // handle the event queue to send messages
  while (!eventQueue.empty())
  {
    // handle the sensorEvent event
    sid = eventQueue.top().getID();
    st = eventQueue.top().getTime();
    usleep( (st - time) * sleepConversion);
    time = st;
    eventQueue.pop();

    // test if sensor has failed
    if ( sensorArray[sid].getActive() )
    {
      failCheck = getRandDble();
      if (failCheck < failureProb)
      {
        std::cout << "***sensor #" << sid << " FAILED at time = " << time << " sec\n";
        sensorArray[sid].setActive(false);
        numFailed += 1;
        for (int j = 0; j < NDATA; j++)
        {
          sensorArray[sid].setData(j, -1.0);
        }
      }
      else
      {
        //std::cout << "sensor #" << sid << " records new data at time = " << time << " sec \n";
        for (int j = 0; j < NDATA; j++)
        {
          sensorArray[sid].setData(j, 1.0);
        }         
      }
    }

    // send current data
    sensorArray[sid].fillDataContainer(time, dataToSend);
    channel = channelPrefix + std::to_string(sid);
    lcm.publish(channel, &dataToSend);

    // add a new event to the sensor queue
    dt = (getRandDble() * tnom) + tnom;
    if ( (time + dt) < tmax)
    {
      eventQueue.push( SensorEvent(sid, time + dt) );
    }
  }

  // print summary statistics
  std::cout << "\n  *SENSOR SIMULATOR SUMMARY* \n";
  std::cout << "\t" << numFailed << " sensors failed\n";
  std::cout << "\t" << numSensors << " total sensors\n";
  std::cout << "\t" << ( (double)numFailed / (double)numSensors) * 100.0 << "% failure rate\n";
  printf("\t%.3f total time [sec]\n", time );
  printf("\t%.3f failed per sec\n\n", (double)numFailed / time );

  return 0;
}