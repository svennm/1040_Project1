#include <iostream>
#include <iomanip>
#include "passengers.h"
#include "drivers.h"
// #include "riders.h"

using namespace std;

void PrintMenu(){
    cout << "MENU\n";
    cout << "A - Add Item\n";
    cout << "E - Edit\n";
    cout << "D - Delete\n";
    cout << "F - Find\n";
    cout << "S - Print Single Entity\n";
    cout << "P - Print All Entries in Collection\n";


}

void ExecuteMenu(char option, drivers& ListOfDrivers, passengers& ListOfPassengers){
char c = ' ';
int tempNum = 0;
string tempStr = " ";
bool tempBool = 0;
float tempFloat = 0.0;
driver d;
passenger p;


    switch (toupper(option))
    {
        case 'A':
        cin.ignore();
        cout << "Choose what list to add too.\n";
        cout << "A. Drivers\n" << "B. Passengers\n" << "C. Rides\n";
        cin >> c;

            switch (toupper(c))
            {
            case 'A':
            cin.ignore();
            
            cout <<"Enter ID: ";
            cin >> tempNum;
            d.setID(tempNum);
            cin.ignore();

            cout <<"Enter Name: ";
            getline(cin, tempStr);
            d.setName(tempStr);
            cin.ignore();

            cout <<"Enter Vehicle Capacity: ";
            cin >> tempNum;
            d.setCapacity(tempNum);
            cin.ignore();

            do{
            cout <<"Handicap Capable, Please Enter yes or no: ";
                
                    cin >> tempStr;
                    if(tempStr == "yes"){
                        tempBool = true;
                        d.setHandicap(tempBool);
                    }
                    else if(tempStr == "no"){
                        tempBool = false;
                        d.setHandicap(tempBool);
                    }
                    else{
                        cout << "Please input yes or no";
                    }
            }
            while(tempStr != "yes" || tempStr != "no");
            cin.ignore();

            do{
            cout <<"Please enter the veichle type of: compact, 2dr, sedan, 4dr, SUV, van, other";
                cin >> tempStr;
                d.setType(tempStr);
                                    
             
            }
            while(tempStr != "compact" || tempStr != "2dr" || tempStr != "sedan" ||tempStr != "4dr" || tempStr != "SUV" || tempStr != "van" || tempStr != "other");
            cin.ignore();

            do{
            cout << "Driver Rating Between 1 and 5: ";
            cin >> tempFloat;
            d.setRating(tempFloat);

            }
            while(tempFloat < 1 || tempFloat > 5);
            cin.ignore();

            do{
            cout <<"Available, Please Enter yes or no: ";
                
                    cin >> tempStr;
                    if(tempStr == "yes"){
                        tempBool = true;
                        d.setAvailable(tempBool);
                    }
                    else if(tempStr == "no"){
                        tempBool = false;
                        d.setAvailable(tempBool);
                    }
                    else{
                        cout << "Please input yes or no";
                    }
            }
            while(tempStr != "yes" || tempStr != "no");
            cin.ignore();

            do{
            cout <<"Pets Allowed, Please Enter yes or no: ";
                
                    cin >> tempStr;
                    if(tempStr == "yes"){
                        tempBool = true;
                        d.setPets(tempBool);
                    }
                    else if(tempStr == "no"){
                        tempBool = false;
                        d.setPets(tempBool);
                    }
                    else{
                        cout << "Please input yes or no";
                    }
            }
            while(tempStr != "yes" || tempStr != "no");
            cin.ignore();

            cout <<"Important Notes: ";
            getline(cin, tempStr);
            d.setNotes(tempStr);
            cin.ignore();


            ListOfDrivers.Add(d);
            cout <<"\n";

            break;

            case 'B':
            cin.ignore();
            
            cout << "Enter Name: ";
            getline(cin, tempStr);
            p.setName(tempStr);
            cin.ignore();

            cout <<"Enter ID: ";
            cin >> tempNum;
            p.setID(tempNum);
            cin.ignore();

            do{
            cout << "Enter Payment Method(cash, card, debit): ";
            cin >> tempStr;
            p.setPaymentMethod(tempStr);
            
            }
            while(tempStr != "cash" || tempStr != "card"|| tempStr != "debit");
            cin.ignore();

            do{
            cout <<"Handicapped, Please Enter yes or no: ";
                
                    cin >> tempStr;
                    if(tempStr == "yes"){
                        tempBool = true;
                        p.setHandicap(tempBool);
                    }
                    else if(tempStr == "no"){
                        tempBool = false;
                        p.setHandicap(tempBool);
                    }
                    else{
                        cout << "Please input yes or no";
                    }
            }
            while(tempStr != "yes" || tempStr != "no");
            cin.ignore();

            do{
            cout << "Passenger Rating Between 1 and 5: ";
            cin >> tempFloat;
            p.setRating(tempFloat);

            }
            while(tempFloat < 1 || tempFloat > 5);
            cin.ignore();

            do{
            cout <<"Pets with you, Please Enter yes or no: ";
                
                    cin >> tempStr;
                    if(tempStr == "yes"){
                        tempBool = true;
                        p.setPets(tempBool);
                    }
                    else if(tempStr == "no"){
                        tempBool = false;
                        p.setPets(tempBool);
                    }
                    else{
                        cout << "Please input yes or no";
                    }
            }
            while(tempStr != "yes" || tempStr != "no");
            cin.ignore();

            ListOfPassengers.Add(p);
            cout <<"\n";
            break;

            // case 'C'     
           

        
        }
        
        break;
    
    //case 'E':

    }
    

}




int main() {
    string name, name2;

    char c;
    name = "Passengers List";
    name2 = "Drivers List";
    

    cout << name <<"\n";
    passengers p_list(name);
    drivers d_list(name2);
    c = ' ';

    PrintMenu();
    while(c != 'q'){
        cout << "Option Choice\n";
        cin >> c;
        if (c == 'A' || c == 'd'|| c == 'f'|| c == 'p'){
            ExecuteMenu(c, d_list, p_list);
            PrintMenu();
        }

    }
    return 0;
}


