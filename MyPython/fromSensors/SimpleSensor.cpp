/* 01-11-17
   Takes completed FDS_output.dat and produces small data 
   packages update.dat for each step

   $ g++ SimpleSensor.cpp -o SimpleSensor.exe
   $ ./SimpleSensor.exe

   (make sure the FDS_output.dat file is in the same directory)
 
*/

#include <iostream>
#include <fstream>
#include <math.h>
#include <string>
#include <sstream>
#include <string>
#include <unistd.h>

using namespace std;

int main () {

  // initialize the data table
  const int ROWS = 300;
  const int COLS = 3;
  double inData[ROWS][COLS];
  const int MAX_STEPS = 300;

  // select data file
  ifstream file("FDS_output.dat");
  string line;

  // read in line-by-line of the FDS data
  double readValue;
  int i, j;
  i = 0;
  while (getline(file, line)) {
    istringstream iss(line);
    j = 0;
    while (iss >> readValue) {
      //cout << "value = " << readValue << " at (" << i << ", " << j << ")" << '\t';
      inData[i][j] = readValue;
      j++;
    }
    i++;
    //cout << endl;
  }
  file.close();

  // generate a data package for each time step
  for (int iTime = 0; iTime < MAX_STEPS; iTime++) {
    string filename = "update";
    filename = filename + ".dat";
    ofstream myfile;
    myfile.open (filename.c_str());
    for (int jCols = 0; jCols < COLS; jCols++) {
      myfile << inData[iTime][jCols] << "\t" << "\t";
    }
    myfile << "\n";
    myfile.close();
    cout << "finished step #" << iTime << " with t = " << inData[iTime][0] << endl;
    usleep( 1.0 * pow(10.0, 6.0) );
  }

  return 0;
}
