#include "driver.h"

driver::driver(){

    d_id = 0;
    d_name = "None";
    v_capacity = 0;
    handicap = 0;
    v_type = "Blank";
    d_rating = 0.0;
    v_available = 0;
    pets = 0;
    notes = "Blank";


}

driver::driver(int d_id, string d_name, int v_capacity, bool handicap, string v_type, float d_rating, bool v_available, bool pets, string notes){
this -> d_id = d_id;
this -> d_name = d_name;
this -> v_capacity = v_capacity;
this -> handicap = handicap;
this -> v_type = v_type;
this -> d_rating = d_rating;
this -> v_available = v_available;
this -> pets = pets;
this -> notes = notes;
}

void driver::setID(int i){
    d_id = i;
}

void driver::setName(string n){
    d_name = n;
}

void driver::setCapacity(int i){
    v_capacity = i;
}

void driver::setHandicap(bool b){
    handicap = b;
}

void driver::setType(string t){
    v_type = t;
}

void driver::setRating(float r){
    d_rating = r;
}

void driver::setAvailable(bool b){
    v_available = b;
}

void driver::setPets(bool b){
    pets = b;
}
void driver::setNotes(string n){
    notes = n;
}

int driver::getID() const{
    return d_id;
}

string driver::getName() const{
    return d_name;
}

int driver::getCapacity() const{
    return v_capacity;
}

bool driver::getHandicap() const{
    return handicap;
}

string driver::getType() const{
    return v_type;
}

float driver::getRating() const{
    return d_rating;
}

bool driver::getAvailable() const{
    return v_available;
}

bool driver::getPets() const{
    return pets;
}

string driver::getNotes() const{
    return notes;
}