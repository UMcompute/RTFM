#include <stdio.h>
#include "SensorEvent.h"

SensorEvent::SensorEvent(
      int inID, 
      double inTime)
{
  // set the sensor's ID corresponding to this event
  if (inID < 0)
  {
    printf("\n***error: sensor ID number should not be negative: %d \n", inID);
    ID = 1000;
  }
  else
  {
    ID = inID;
  }

  // set the time that this event will take place
  if (inTime < 0.0)
  {
    printf("\n***error: event time should not be negative: %f \n", inTime); 
    time = 1000.0;
  }
  else
  {
    time = inTime;
  }
}

int SensorEvent::getID() const
{
  return ID;
}

double SensorEvent::getTime() const
{
  return time; 
}
