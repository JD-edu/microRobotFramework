#include "microRobotFramework.hpp"
#include <fcntl.h>    // For O_RDWR, O_NOCTTY, etc.
#include <unistd.h>   // For close()
#include <termios.h>  // For configuring serial port settings
#include <cstring>    // For memset()
#include <iostream>



// Constructor
MRF::MRF(const std::string& port, int baud)
    : serial_port(port), baud_rate(baud_rate), connected(false),
      accel_x(0), accel_y(0), accel_z(0),
      gyro_x(0), gyro_y(0), gyro_z(0),
      pitch(0), roll(0), yaw(0),
      encoder1(0), encoder2(0), encoder3(0), encoder4(0) {
    serial_port = port;
    baud_rate = baud;

    connected = openSerial();
}

bool MRF::receiveSensorData(){
    uint8_t buffer[23];
    int bytesRead = read(serial_fd, buffer, 23);
    //std::cout << "test\n"; for debugging, but it take long time to execute.
    if(bytesRead != 23 ){
        return 0;
    }

    accel_x = (buffer[2] << 8) | buffer[3];
    accel_y = (buffer[4] << 8) | buffer[5];
    accel_z = (buffer[6] << 8) | buffer[7];
    gyro_x = (buffer[8] << 8) | buffer[9];
    gyro_y = (buffer[10] << 8) | buffer[11];
    gyro_z = (buffer[12] << 8) | buffer[13];
    encoder1 = (buffer[14] << 8) | buffer[15];
    encoder2 = (buffer[16] << 8) | buffer[17];
    encoder3 = (buffer[18] << 8) | buffer[19];
    encoder4 = (buffer[20] << 8) | buffer[21];

    // Print received acceleration X value
    //std::cout << "X: " << accel_x << " Y: " << accel_y << " Z: "<< accel_z;
    //std::cout << " X: " << gyro_x << " Y: " << gyro_y << " Z: "<< gyro_z;
    //std::cout << " 1: " << encoder1 << " 2: " << encoder2 << " 3: "<< encoder3 << " 4: " << encoder4 << std::endl;

    return 1;
}

bool MRF::sendMotorCommand(int speed, int angle) {
    if (!connected) {
        std::cerr << "Serial port not connected!" << std::endl;
        return false;
    }

    // Packet structure: [Header][Length][Speed][Angle][Checksum]
    uint8_t packet[5];
    packet[0] = 0xAA;  // Header byte (example: 0xAA, can be changed)
    packet[1] = 3;     // Length byte (number of data bytes: speed + angle + checksum)
    packet[2] = speed & 0xff; // Speed byte (0-255)
    packet[3] = angle & 0xff; // Angle byte (-127 to 127)
    packet[4] = packet[0] ^ packet[1] ^ packet[2] ^ packet[3]; // Simple XOR checksum

    // Send packet over serial
    int bytesWritten = write(serial_fd, packet, sizeof(packet));
    if (bytesWritten != sizeof(packet)) {
        std::cerr << "Failed to send motor command!" << std::endl;
        return false;
    }

    return true;
}


bool MRF::openSerial(){

    // Open serial port
    serial_fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY);
    if (serial_fd == -1) {
        std::cerr << "Error opening serial port" << std::endl;
        connected = false;
        return 0;
    }else{
        std::cout << "Serial port opened! "<<  serial_fd  << std::endl;
        connected = true;
    }

    // Configure serial port
    struct termios options;
    tcgetattr(serial_fd, &options);
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);
    options.c_cflag = CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(serial_fd, TCIFLUSH);
    tcsetattr(serial_fd, TCSANOW, &options);

    return 1;

}

bool MRF::isConnected(){
    return  connected;
}

int16_t MRF::getAccelX(){
    return accel_x;
}

int16_t MRF::getAccelY(){
    return accel_y;
}

int16_t MRF::getAccelZ(){
    return accel_z;
}

int16_t MRF::getGyroX(){
    return gyro_x;
}

int16_t MRF::getGyroY(){
    return gyro_y;
}

int16_t MRF::getGyroZ(){
    return gyro_z;
}

uint16_t MRF::getEncoder1(){
    return encoder1;
}

uint16_t MRF::getEncoder2(){
    return encoder2;
}

uint16_t MRF::getEncoder3(){
    return encoder3;
}

uint16_t MRF::getEncoder4(){
    return encoder4;
}