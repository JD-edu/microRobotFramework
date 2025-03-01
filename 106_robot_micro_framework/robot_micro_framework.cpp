#include "robot_micro_framework.hpp"
#include <iostream>
#include <unistd.h>  // For sleep
#include <cstring>   // For memset
#include <termios.h> // Serial settings
#include <unistd.h> // POSIX API for serial
#include <fcntl.h>  // File control for serial

// Constructor
RobotFrameWork::RobotFrameWork() : serial_fd(-1) {}

// Destructor
RobotFrameWork::~RobotFrameWork() {
    if (serial_fd != -1) {
        close(serial_fd);
        std::cout << "Serial port closed." << std::endl;
    }
}

// Initialize Serial Communication
void RobotFrameWork::initSerial(const char* port) {
    serial_fd = open(port, O_RDWR | O_NOCTTY | O_SYNC);
    if (serial_fd == -1) {
        throw std::runtime_error("Failed to open serial port");
    }

    // Get current terminal attributes
    if (tcgetattr(serial_fd, &tty) != 0) {
        close(serial_fd);
        throw std::runtime_error("Failed to get serial port attributes");
    }

    // Configure baud rate (e.g., 9600)
    cfsetospeed(&tty, B9600);
    cfsetispeed(&tty, B9600);

    // Configure 8N1 (8 data bits, No parity, 1 stop bit)
    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;
    tty.c_cflag |= (CLOCAL | CREAD); // Enable receiver, set local mode
    tty.c_cflag &= ~PARENB;          // No parity
    tty.c_cflag &= ~CSTOPB;          // 1 stop bit
    tty.c_cflag &= ~CRTSCTS;         // No hardware flow control

    // Configure raw input mode
    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // No software flow control
    tty.c_oflag &= ~OPOST;                  // Raw output

    // Apply attributes
    if (tcsetattr(serial_fd, TCSANOW, &tty) != 0) {
        close(serial_fd);
        throw std::runtime_error("Failed to set serial port attributes");
    }

    std::cout << "Serial port initialized: " << port << std::endl;
}

// Read Serial Data
void RobotFrameWork::serialRead(uint8_t* buffer, int size) {
    if (serial_fd == -1) {
        throw std::runtime_error("Serial port not initialized");
    }

    int bytesRead = read(serial_fd, buffer, size);
    if (bytesRead < 0) {
        throw std::runtime_error("Failed to read from serial port");
    }else if (bytesRead == 6) {
        int16_t accelX, accelY, accelZ;
        memcpy(&accelX, buffer, 2);
        memcpy(&accelY, buffer + 2, 2);
        memcpy(&accelZ, buffer + 4, 2);

        //std::cout << std::fixed << std::setprecision(3);
        std::cout << "roll: " << accelX 
                << ", pitch: " << accelY 
                << ", yaw: " << accelZ << std::endl;
    }


    std::cout << "Received: ";
    for (int i = 0; i < bytesRead; i++) {
        std::cout << std::hex << static_cast<int>(buffer[i]) << " ";
    }
    std::cout << std::endl;
}

// === Application Main Function ===
int main() {
    RobotFrameWork robot;
    const char* serialPort = "/dev/ttyUSB0";  // Change this to your actual port

    try {
        robot.initSerial(serialPort);

        uint8_t buffer[6];  // Buffer to store received data
        memset(buffer, 0, sizeof(buffer));

        while (true) {
            robot.serialRead(buffer, sizeof(buffer));
            sleep(1);  // Wait for next read (adjust based on your needs)
        }

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
