#ifndef PASSENGERS_H
#define PASSENGERS_H
#include <vector>
#include <string>
#include <iterator>
using namespace std;

#include "passenger.h"

class passengers{
    private:
    vector<passenger> TotalPassengers;
    string ListName;

    public:
    passengers();
    passengers(string);
    void Add(passenger p);
    void PrintSize();
    void PrintAll();
    void FindEntry(int n) ;

};
#endif