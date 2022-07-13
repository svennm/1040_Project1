#include "drivers.h"
#include <iterator>
drivers::drivers(){

}

drivers::drivers(string name){
    ListName = name;
} 

void drivers::Add(driver driver1){
    TotalDrivers.push_back(driver1);
}

void drivers::PrintSize(){
    if(TotalDrivers.size() != 0){
    cout <<"The is currently " <<TotalDrivers.size() << " Drivers";
    }
    else
    cout << "vector is empty man!\n";
}





