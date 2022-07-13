#ifndef DRIVER_H
#define DRIVER_H
#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

class driver{
private:
    int d_id;
    string d_name;
    int v_capacity;
    bool handicap;
    string v_type;
    float d_rating;
    bool v_available;
    bool pets;
    string notes;

public:
    driver();
    driver(int, string, int, bool, string, float, bool, bool, string);
    void setID(int);
    void setName(string);
    void setCapacity(int);
    void setHandicap(bool);
    void setType(string);
    void setRating(float);
    void setAvailable(bool);
    void setPets(bool);
    void setNotes(string);

    int getID() const;
    string getName() const;
    int getCapacity() const;
    bool getHandicap() const;
    string getType() const;
    float getRating() const;
    bool getAvailable() const;
    bool getPets() const; 
    string getNotes() const;


    


};


#endif
