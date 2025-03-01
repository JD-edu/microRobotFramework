#include "microRobotFramework.hpp"
#include <iostream>
#include <unistd.h>

int main(){

    int count = 0;
    bool ret = false;
    MRF mrf("/dev/ttyUSB0", 115200);

    if(!mrf.isConnected()){
        std::cout << "Serial port is not connected" << std::endl;
        return 0;
    }
    while(true){
        ret = mrf.receiveSensorData();
        if(ret){
            std::cout << mrf.getAccelX() << "  " << mrf.getAccelY() << "  " << mrf.getAccelZ() << std::endl;
        }  
        usleep(1000);     
        /*
        Cooling down. If we send motor command with short interval, 
        Arduino serial buffer is freezed. 
        Below code is just study and test purpose only. 
        Use thread to receiving IMU and send motor command at same time 
        */
        if(count++ > 100){
            mrf.sendMotorCommand(90, 100);
            count = 0;
        }
            
    }
}