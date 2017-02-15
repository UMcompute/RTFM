// How to compile and run this code via terminal:
// $ g++ -o recver recver.cpp -llcm -std=c++11
// $ ./recver

// C++ preprocessor directives
#include <iostream>
#include <stdio.h>
#include <queue>
#include <sys/select.h>
#include <ctime>
#include <math.h>
#include <unistd.h>
#include <chrono>

// additional LCM directives
#include <lcm/lcm-cpp.hpp>
#include "toEDM/edm.hpp"
#include "frEDM/edmOUT.hpp"

// namespace declarations
using namespace std;

// LCM class for receiving message data
class Handler
{

private:
  double myTime;
  double myFlux;
  double myTemp;

public:
  ~Handler() {}

  void handleMessage(const lcm::ReceiveBuffer* rbuf,
		     const std::string& chan,
		     const toEDM::edm* msg)
  {
    //printf("\n");
    //printf("~~~~EDM Received message on channel \"%s\":\n", chan.c_str());
    printf("   EDM Current Time: %f\n", msg->time);
    //printf("Net Flux:     %f\n", msg->flux);
    //printf("Temperature:  %f\n", msg->temp);
    //printf("\t %f \t %f \t %f\n", msg->time, msg->flux, msg->temp);
    myTime = msg->time;
    myTemp = msg->temp;
    myFlux = msg->flux;
  }

  double getTime() { return myTime; }
  double getFlux() { return myFlux; }
  double getTemp() { return myTemp; }

};


// global function heading
double computeRegressionSlope(queue<double> inX, queue<double> inY);




// MAIN PROGRAM
int main(int argc, char** argv) {

  // construct LCM and check if it is good!
  lcm::LCM lcm;
  if(!lcm.good()) return 1;

  // construct a Handler and subsribe to receive messages
  Handler handlerObject;
  lcm.subscribe("EDM_CHAN", &Handler::handleMessage, &handlerObject);

  // generate new queues to hold incoming data
  const int MAX_MSG_LIMIT = 1000;
  const int MAX_QUEUE_SIZE = 5;
  queue<double> fluxQueue;
  queue<double> fluxMAQ;
  double fluxSum = 0.0;
  queue<double> tempQueue;
  queue<double> tempMAQ;
  double tempSum = 0.0;
  queue<double> timeQueue;
  double waitUsec = 2.5;

  // data structure to send output back to main program
  frEDM::edmOUT sendToMain;

  // make a blocking hold to wait for messages and process their info
  //while(0 == lcm.handle()) {

  // New 02-10-17 :: Use the select function to manage messages instad
  int numMsgRecv = 0;
  //while (1)
  while (numMsgRecv < MAX_MSG_LIMIT)
  {
    // setup the LCM file descriptor for waiting
    int lcm_fd = lcm.getFileno();
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(lcm_fd, &fds);

    // wait a limited amount of time for an incoming msg
    struct timeval timeout = {
      5,  // seconds
      0   // microseconds
    };
    int status = select(lcm_fd + 1, &fds, 0, 0, &timeout);
    //std::cout << "status = " << status << "\n";

    // interpret status
    if (0 == status)
    {
      // no msg yet!
      printf("\n   [waiting for msg in EDM main loop] \n");
    }
    else if (FD_ISSET(lcm_fd, &fds))
    {
      // LCM has events for you to process!
      lcm.handle();
      //printf("   new msg in EDM! \n");
      //numMsgRecv += 1;
      //cout << " *** " << endl;
      //cout << "total messages received: " << numMsgRecv << endl;
      //cout << " *** " << endl;
    


      // do some work using the new data ...
      //   (compute x)

      // store the current values obtained from the message
      double currTime = handlerObject.getTime();
      double currFlux = handlerObject.getFlux();
      double currTemp = handlerObject.getTemp();

      // queues are not full yet
      if (fluxQueue.size() < MAX_QUEUE_SIZE) {

          // time
          timeQueue.push(currTime);

          // flux
          fluxQueue.push(currFlux);
          fluxSum += fluxQueue.back();
          fluxMAQ.push(fluxSum / fluxQueue.size());

          // temperature
          tempQueue.push(currTemp);
          tempSum += tempQueue.back();
          tempMAQ.push(tempSum / tempQueue.size());

      }
      // queues are full (i.e., for all steps later than MAX_QUEUE_SIZE)
      else {

          // time
          timeQueue.pop();
          timeQueue.push(currTime);

          // flux
          fluxSum -= fluxQueue.front();
          fluxQueue.pop();
          fluxQueue.push(currFlux);
          fluxSum += fluxQueue.back();
          fluxMAQ.pop();
          fluxMAQ.push(fluxSum / MAX_QUEUE_SIZE);

          // temperature
          tempSum -= tempQueue.front();
          tempQueue.pop();
          tempQueue.push(currTemp);
          tempSum += tempQueue.back();
          tempMAQ.pop();
          tempMAQ.push(tempSum / MAX_QUEUE_SIZE);

      }

      // linear regression fit of unsmoothed and smoothed data sets
      double slopeOfTemp = computeRegressionSlope(timeQueue, tempQueue);

      printf("wait ...\n");
      usleep( waitUsec * pow(10.0, 6.0) );
      printf("... done waiting! \n");

      // create LCM message to send back to MAIN
      sendToMain.tempSlope = slopeOfTemp;
      lcm.publish("OUT_EDM", &sendToMain);

      // print the current step results
      //cout << currTime << " " << currFlux << " " << currTemp << " ";
      //cout << slopeOfTemp << " " << endl;

    }

    // should provide some exit criteria!
  }
  //}

  // if successful, main program returns zero
  return 0;
}



// global function definition
double computeRegressionSlope(queue<double> inX, queue<double> inY)
{
    // initialize the local variable and constant
    double slope = 0.0;
    const int N = inX.size();

    // compute the summed components
    double x = 0.0;
    double y = 0.0;
    double sumXX = 0.0;
    double sumXY = 0.0;
    double sumX = 0.0;
    double sumY = 0.0;
    while(!inX.empty()) {
        x = inX.front();
        inX.pop();
        y = inY.front();
        inY.pop();
	//	cout << x << " " << y << " " << N << " " << endl;
        sumXX += x * x;
        sumXY += x * y;
        sumX  += x;
        sumY  += y;
    }

    // compute the slope of the regression line
    slope = (sumXY - sumX * sumY / N) / (sumXX - sumX * sumX / N);
    if (slope > 0.0 || slope <= 0.0)
    {
      // good!
    }
    else
    {
      // then slope is NaN
      slope = 0.0;
    }

    return slope;
}
