#include <iostream>
#include <iomanip>

using namespace std;

#include "drivers.h"

void PrintMenu(){
    cout << "MENU \n";
    cout << "a - Add item\n";
    cout << "d - remove  item\n";
    cout << "f - get num items\n";

}

void ExecuteMenu(char option, drivers& ListOfDrivers){
    int d_id;
    string d_name;
    int v_capacity;
    bool handicap;
    string v_type;
    float d_rating;
    bool v_available;
    bool pets;
    string notes;
    driver driver1;

    switch(option){
        case 'a':
            cin.ignore();
            cout << "Add to drivers\n";
            cout << "Enter ID: ";
            cin >> d_id;
            cin.ignore();
            cout << "Enter Name: ";
            getline(cin, d_name);
            cout << "Veichle Capacity: ";
            cin >> v_capacity;
            cin.ignore();
            cout << "Handicap Friendly(1 for yes, 0 for no)\n";
            cin >> handicap;
            cin.ignore();
            cout << "Type of Car: ";
            getline(cin, v_type);
            cout << "Rating of driver: ";
            cin >> d_rating;
            cout << endl;
            cin.ignore();
            cout << "Available: ";
            cin >> v_available;
            cout << endl;
            cin.ignore();
            cout << "Pets allowed?\n";
            cin >> pets;
            cin.ignore();
            cout <<"Any notes?\n";
            getline(cin, notes);
            

            driver1.setID(d_id);
            driver1.setName(d_name);
            driver1.setCapacity(v_capacity);\
            driver1.setHandicap(handicap);
            driver1.setType(v_type);
            driver1.setRating(d_rating);
            driver1.setAvailable(v_available);
            driver1.setPets(pets);
            driver1.setNotes(notes);

            ListOfDrivers.Add(driver1);
            cout << "\n";
        break;

        case 'f':
            ListOfDrivers.PrintSize();

        break;    


            

            

    }




}
int main() {
    string name;
    char c;

    cout << "List Name:\n";
    getline(cin, name);

    drivers List(name);
    c = ' ';

    PrintMenu();
    while(c != 'q'){
        cout << "Option choice:\n";
        cin >> c;
        if (c == 'a' || c == 'd'|| c == 'f'){
            ExecuteMenu(c, List);
            PrintMenu();
        }
    }
    return 0;

}


