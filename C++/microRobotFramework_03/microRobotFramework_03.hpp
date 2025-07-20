#ifndef MRF_H
#define MRF_H

#include <string>
#include <vector>
#include <cstdint>

class MRF {
public:
    // Constructor & Destructor
    MRF(const std::string& port, int baud_rate);

    // Sensor Data Reception (IMU + Encoder)
    bool receiveSensorData();  // Reads both IMU and encoder data from serial
    //void getOrientation(float &pitch, float &roll, float &yaw) const;
    //void getWheelSpeeds(float &left_speed, float &right_speed) const;

    // Motor Control
    bool sendMotorCommand(int speed, int angle);

    // Sensor Processing
    //bool processCameraData();  // Handle camera frames
    //bool processLidarData();   // Process LiDAR scan data

    // Serial Communication
    bool isConnected();
    void closeConnection();

    int16_t getAccelX();
    int16_t getAccelY();
    int16_t getAccelZ();
    int16_t getGyroX();
    int16_t getGyroY();
    int16_t getGyroZ();
    uint16_t getEncoder1();
    uint16_t getEncoder2();
    uint16_t getEncoder3();
    uint16_t getEncoder4();

private:
    // Serial Communication
    int serial_fd;  // File descriptor for serial port
    std::string serial_port;
    int baud_rate;
    bool connected;

    // IMU Data
    int16_t accel_x, accel_y, accel_z;
    int16_t gyro_x, gyro_y, gyro_z;
    float pitch, roll, yaw;

    // Encoder Data
    uint16_t encoder1, encoder2, encoder3, encoder4;

    // Private Helpers
    bool openSerial();
    //bool readSerialData(std::vector<uint8_t>& buffer, size_t length);
    //bool writeSerialData(const std::vector<uint8_t>& buffer);
    //void parseSensorData(const std::vector<uint8_t>& buffer);  // Parses both IMU & Encoder
};

#endif // MRF_H
