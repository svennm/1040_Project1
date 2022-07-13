#include "passenger.h"

passenger::passenger(){

}

passenger::passenger(string name, int id, string p_method, bool handicap, float rating, bool pets) {
    this -> name = name;
    this -> id = id;
    this -> p_method = p_method;
    this -> handicap = handicap;
    this -> rating = rating;
    this -> pets = pets;
}

void passenger::setName(string n){
    name = n;
}

void passenger::setID(int i){
    id = i;
}

void passenger::setPaymentMethod(string p){
    p_method = p;
}

void passenger::setHandicap(bool b){
    handicap = b;
}

void passenger::setRating(float f){
    rating = f;
}

void passenger::setPets(bool b){
   pets = b;
}

/* void passenger::PrintObject(passenger* it) {
    cout << "Name is " << name << endl;
    cout << "ID is " << id << "\n";
    cout << "Payment Method " << p_method << "\n";
    if(handicap == 1){
        cout << "Handicap Capable" << "\n";
    } 
    else {
        cout << "Not Handicap Capable" << "\n";
    }
    cout << "Rider Rating is " << rating <<"\n";
    if(pets == 1){
        cout << "Pet Capable" << "\n";
    } 
    else {
        cout << "Not Pet Capable" << "\n";
    }
}
*/


string passenger::getName() const{
    return name;
}

int passenger::getID() const{
    return id;
}

string passenger::getPayment() const{
    return p_method;
}

bool passenger::getHandicap() const{
    return handicap;
}

float passenger::getRating() const{
    return rating;
}

bool passenger::getPets() const{
    return pets;
}




