#include "microRobotFramework.hpp"
#include <iostream>
#include <unistd.h>

/*
g++ -o mrf_example_01 mrf_example_01.cpp microRobotFramework.cpp -std=c++11
*/

int main(){

    bool ret = false;
    MRF mrf("/dev/ttyACM0", 115200);

    if(!mrf.isConnected()){
        std::cout << "Serial port is not connected" << std::endl;
        return 0;
    }
    while(true){
        ret = mrf.receiveSensorData();
        if(ret){
            std::cout << mrf.getAccelX() << "  " << mrf.getAccelY() << "  " << mrf.getAccelZ() << std::endl;
        }  
        usleep(5000);     
    }
}