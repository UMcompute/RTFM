#ifndef SENSOREVENT_H_INCLUDED
#define SENSOREVENT_H_INCLUDED

class SensorEvent
{
  private:
    int ID;
    double time;

  public:
    SensorEvent(int inID, double inTime);
    int getID() const;
    double getTime() const;
};

#endif  // SENSOREVENT_H_INCLUDED