
//determine OS
#ifdef __unix__         
    #define OS_Unix
#elif defined(_WIN32) || defined(WIN32) 
    #define OS_Windows
#endif


#ifdef OS_Unix
    #include <sys/socket.h> 
    #include <arpa/inet.h> 
    #include <unistd.h> 
#endif

#ifdef OS_Windows

#endif


class Connector{
public:
    Connector(char *ip, int port);
    ~Connector();

    int Connect();
    int get();
    int write(char* str, int len);


    void displayError(int no);

    char _stagerIP[25];
    int _stagerPort;
    char buffer[1024];
private:
    char *_conIP;
    int _conPort;

    int sock;
};