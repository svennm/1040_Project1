#include <iostream>
#include <iomanip>
using namespace std;

#include "passengers.h"

void PrintMenu(){
    cout << "MENU \n";
    cout << "a - Add item\n";
    cout << "d - remove  item\n";
    cout << "f - get num items\n";
    cout << "P - print all\n";
}


void ExecuteMenu(char option, passengers& ListOfPassengers){
    string name;
    int id;
    string p_method;
    bool handicap;
    float rating;
    bool pets;
    passenger p;

    switch(option){
        case 'a':
            cin.ignore();
            cout << "Add To Passengers\n";
            cout <<"Enter Name: ";
            getline(cin, name);
            cout << endl;
            cout << "Enter ID: ";
            cin >> id;
            cout << endl;
            cin.ignore();
            cout << "Payment Method: ";
            getline(cin, p_method);
            cout << "\n";
            cout << "Handicap: (1 for yes, 0 for no): ";
            cin >> handicap;
            cout << endl;
            cout << "Rating: ";
            cin >> rating;
            cout << endl;
            cin.ignore();
            cout << "Pets: ";
            cin >> pets;
            cout << endl;
            cin.ignore();
        
            p.setID(id);
            p.setName(name);
            p.setPaymentMethod(p_method);
            p.setHandicap(handicap);
            p.setRating(rating);
            p.setPets(pets);


        ListOfPassengers.Add(p);
        cout << "\n";
        break;

        case 'f':
        ListOfPassengers.PrintSize();
        break;

        case 'p':
        ListOfPassengers.PrintAll();
        break;    
    }
}




int main() {
    string name;
    char c;
    name = "Passengers List";

    cout << name <<"\n";
    passengers List(name);
    c = ' ';

    PrintMenu();
    while(c != 'q'){
        cout << "Option Choice\n";
        cin >> c;
        if (c == 'a' || c == 'd'|| c == 'f'|| c == 'p'){
            ExecuteMenu(c, List);
            PrintMenu();
        }

    }
    return 0;
}