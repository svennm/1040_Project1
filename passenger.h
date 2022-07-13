#ifndef PASSENGER_H
#define PASSENGER_H
#include <string>
#include <iostream>
using namespace std;
class passenger{
    private:
        string name;
        int id;
        string p_method;
        bool handicap;
        float rating;
        bool pets;
    
    public:
        passenger();
        passenger(string name, int id, string p_method, bool handicap, float rating, bool pets);
        void setName(string);
        void setID(int);
        void setPaymentMethod(string);
        void setHandicap(bool);
        void setRating(float);
        void setPets(bool);
        
        
        string getName() const;
        int getID() const;
        string getPayment() const;
        bool getHandicap() const;
        float getRating() const;
        bool getPets() const;

    
};
#endif