#ifndef DRIVERS_H
#define DRIVERS_H
#include <vector>
#include <string>
#include <iterator>
using namespace std;

#include "driver.h"

class drivers{
    private:
    vector<driver> TotalDrivers;
    string ListName;
    
    public:
    drivers();
    drivers(string);
    void Add(driver driver1);
    void PrintSize();
    
    
};
#endif
