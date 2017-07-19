#include <iostream>
#include <ctime>
#include <cstdlib>

int main()
{
  //srand ( time(NULL) );           
  srand(11);
  //just seed the generator

  float min_per = 0.95;
  float max_per = 1.05;
  
  int convFact = 1000000;

  min_per = convFact * min_per + 0.5;
  max_per = convFact * max_per + 0.5; 
  
  int T1 = (int)min_per;
  int T2 = (int)max_per;

  int A = T2 - T1;
  int B = T1;

  int C = rand()%A + B;
  //this produces numbers between T1 and T2

  double random_num = (C*1.0)/convFact;

  std::cout << T1 << "  " << C << "  " << T2 << "\n";
  std::cout << random_num << "\n";

  return 0;
}
