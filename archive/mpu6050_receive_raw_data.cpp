/*
g++ mpu6050_receive_raw_data.cpp -o receive_sensor
*/
#include <iostream>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <cstdint>

int main() {
    const char *portName = "/dev/ttyUSB0"; // Change based on your system

    // Open serial port
    int serialPort = open(portName, O_RDWR | O_NOCTTY);
    if (serialPort == -1) {
        std::cerr << "Error opening serial port" << std::endl;
        return 1;
    }

    // Configure serial port
    struct termios options;
    tcgetattr(serialPort, &options);
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);
    options.c_cflag = CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(serialPort, TCIFLUSH);
    tcsetattr(serialPort, TCSANOW, &options);

    while (true) {
        uint8_t buffer[23];

        // Read 2 bytes from serial
        int bytesRead = read(serialPort, buffer, 23);
        if (bytesRead == 23) {
            //std::cerr << "Error reading from serial port  " << bytesRead << std::endl;
            //continue;
                // Convert received bytes to int16_t (big-endian)
            int16_t accX = (buffer[2] << 8) | buffer[3];
            int16_t accY = (buffer[4] << 8) | buffer[5];
            int16_t accZ = (buffer[6] << 8) | buffer[7];
            int16_t gyroX = (buffer[8] << 8) | buffer[9];
            int16_t gyroY = (buffer[10] << 8) | buffer[11];
            int16_t gyroZ = (buffer[12] << 8) | buffer[13];
            uint16_t encoder1 = (buffer[14] << 8) | buffer[15];
            uint16_t encoder2 = (buffer[16] << 8) | buffer[17];
            uint16_t encoder3 = (buffer[18] << 8) | buffer[19];
            uint16_t encoder4 = (buffer[20] << 8) | buffer[21];

            // Print received acceleration X value
            std::cout << "X: " << accX << " Y: " << accY << " Z: "<< accZ;
            std::cout << " X: " << gyroX << " Y: " << gyroY << " Z: "<< gyroZ;
            std::cout << " 1: " << encoder1 << " 2: " << encoder2 << " 3: "<< encoder3 << " 4: " << encoder4 << std::endl;
        }

       
        //usleep(10000);
    }

    close(serialPort);
    return 0;
}
