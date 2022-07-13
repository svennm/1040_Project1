#include "passengers.h"
#include <iterator>
#include <algorithm>
passengers::passengers(){

}

passengers::passengers(string name){
    ListName = name;

}

void passengers::Add(passenger p){
    TotalPassengers.push_back(p);
}

void passengers::PrintSize(){
    if(TotalPassengers.size() != 0){
        cout << "The size is: " << TotalPassengers.size() << endl;
    }
    else
    cout << "Vector is empty.\n";
}
void passengers::PrintAll(){
    vector<passenger>::iterator it;
    passenger* ptr; 
    unsigned i = 0; // counter
    for(it = TotalPassengers.begin(); it != TotalPassengers.end(); it++, i++) {
       cout << "Name: " << (*it).getName() << endl;
       cout << "ID: " << (*it).getID() << endl;
       cout << "Payment: "<< (*it).getPayment() << endl;
       cout << "Handicap: ";
       if((*it).getHandicap() == 0){
        cout << "Not Handicap Capable \n";
       }
       else{
       cout <<"Handicap Capable \n";
       }
       cout << "Ratings: " <<(*it).getRating() << endl;
       if((*it).getPets() == 0){
        cout << "Not Pet Capable \n";
       }
       else{
       cout <<"Pet Capable \n";
       cout << endl;
       }
    
    }
}

void passengers::FindEntry(int n){
    it = find(TotalPassengers.begin(),TotalPassengers.end(), n);
    cout <<*it <<endl;
}
