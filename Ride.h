#ifndef RIDE_H
#define RIDE_H
#include <string>
#include <iostream>

class ride{
    private:
        int r_id;
        string pickupLocation;
        //confused with time
        string dropoff;
        int sizeofparty;
        bool hasPets;
        //time again
        string status;
    public:
        void setID();
        void setPickUp();
        //not sure how time set would work
        void setDropoff();
        void setPets();
        //time again
        void setStatus();
        int getID();
        string getPickUp();
        //time again
        int getPartySize();
        string getStatus();

}