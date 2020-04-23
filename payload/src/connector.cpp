#include "connector.h"
#include <iostream>



Connector::Connector(char *ip, int port){
    this->_conIP = ip;
    this->_conPort = port;


}





#ifdef OS_Unix

int Connector::connect(){
    this->sock = socket(AF_INET, SOCK_STREAM, 0);
    if (this->sock < 0){  
        return 1;
    } 
}

Connector::~Connector(){}

#endif



void Connector::displayError(int no){
    switch(no){
        case 1:
            std::cout << "Could not create a socket\n";
            break;
        default:
            break;
    }
}





