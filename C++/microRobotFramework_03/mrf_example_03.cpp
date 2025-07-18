#include "microRobotFramework.hpp"
#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>
#include <mutex>

std::atomic<bool> running(true);  // Control loop execution
std::mutex serial_mutex;  // Mutex for serial communication

// Function to receive IMU data in a separate thread
void receiveIMUData(MRF &mrf) {
    while (running) {
        std::lock_guard<std::mutex> lock(serial_mutex);
        if (mrf.receiveSensorData()) {
            std::cout << "AccelX: " << mrf.getAccelX() << " | "
                      << "AccelY: " << mrf.getAccelY() << " | "
                      << "AccelZ: " << mrf.getAccelZ() << std::endl;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(50));  // Adjust reading frequency
    }
}

// Function to send motor commands periodically in a separate thread
void sendMotorCommands(MRF &mrf) {
    int speed = 90;
    int angle = 100;

    while (running) {
        {
            std::lock_guard<std::mutex> lock(serial_mutex);
            mrf.sendMotorCommand(speed, angle);
            //std::cout << "Sent Motor Command: Speed=" << speed << ", Angle=" << angle << std::endl;
        }
        
        std::this_thread::sleep_for(std::chrono::milliseconds(100));  // Send command every 500ms
    }
}

int main() {
    MRF mrf("/dev/ttyUSB0", 115200);

    if (!mrf.isConnected()) {
        std::cout << "Serial port is not connected" << std::endl;
        return 0;
    }

    // Start threads
    std::thread imuThread(receiveIMUData, std::ref(mrf));
    std::thread motorThread(sendMotorCommands, std::ref(mrf));

    // Wait for user input to stop
    std::cout << "Press ENTER to stop..." << std::endl;
    std::cin.get();
    running = false;

    // Join threads before exiting
    imuThread.join();
    motorThread.join();

    return 0;
}
