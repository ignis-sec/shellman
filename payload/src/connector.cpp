#include "connector.h"
#include <iostream>
#include <string.h>


Connector::Connector(char *ip, int port){
    this->_conIP = ip;
    this->_conPort = port;
    strcpy(this->_stagerIP, "localhost");
    this->_stagerPort = 8080;

}





#ifdef OS_Unix

int Connector::Connect(){
    struct sockaddr_in serv_addr;

    this->sock = socket(AF_INET, SOCK_STREAM, 0);
    if (this->sock < 0){  
        return 1;
    }

    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_port = htons(this->_conPort);

    if(inet_pton(AF_INET, this->_conIP, &serv_addr.sin_addr)<=0){ 
        return 2; 
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0){ 
        return 3; 
    }

}

int Connector::write(char* str, int len){
    send(this->sock , str , len , 0 );
}

    int Connector::get(){
        return read( this->sock , this->buffer, 1024);
}

Connector::~Connector(){
    close(this->sock);
}

#endif

#ifdef OS_Windows

int Connector::Connect(){
    return 0;
}

int Connector::write(char* str, int len){
    return 0;
}

int Connector::get(){
    return 0;
}

Connector::~Connector(){
}

#endif













void Connector::displayError(int no){
    switch(no){
        case 1:
            std::cout << "Could not create a socket\n";
            break;
        case 2:
            std::cout << "Invalid address/ Address not supported\n";
            break;
        case 3:
            std::cout << "Connection Failed\n";
            break;
        default:
            break;
    }
}





