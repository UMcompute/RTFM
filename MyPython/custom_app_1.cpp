#include <iostream>
#include <unistd.h>

int main()
{
  unsigned int delay = 1000000;
  int i;
  int n = 10;

  for (i = 0; i < n; i++)
  {
    usleep(delay); 
    std::cout << "i  = " << i << std::endl;
  }

  std::cout << "hello world from c++!" << std::endl;
  return 0;
}

