#ifndef MICRO_FRAMEWORK_H
#define MICRO_FRAMEWORK_H

// Standard includes
#include <iostream>
#include <termios.h>

// Class declaration
class RobotFrameWork {
public:
    RobotFrameWork();            
    ~RobotFrameWork();           // Destructor
    
    void initSerial(const char* port);
    void serialRead(uint8_t* buffer, int size);

private:
    struct termios tty;
    int serial_fd;
};

#endif // MICRO_FRAMEWORK_H
