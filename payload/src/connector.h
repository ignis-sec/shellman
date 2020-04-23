
//determine OS
#ifdef __unix__         
    #define OS_Unix
#elif defined(_WIN32) || defined(WIN32) 
    #define OS_Windows
#endif

#define OS_Unix

#ifdef OS_Unix
    #include <sys/socket.h> 
    #include <arpa/inet.h> 
    #include <unistd.h> 
#endif



class Connector{
public:
    Connector(char *ip, int port);
    ~Connector();
    
    int connect();
    void displayError(int no);

    char *_stagerIP;
    int _stagerPort;
private:
    char *_conIP;
    int _conPort;

    int sock;

    char buffer[1024];
};