#include <iostream>

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