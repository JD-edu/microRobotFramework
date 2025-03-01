### **📜 README.md - Micro Robot Framework (MRF) - Step 1**

# **Micro Robot Framework (MRF) - Step 1: IMU & Encoder Data Reception**
This is the first step in the **Micro Robot Framework (MRF)** tutorial, designed for **robotics education**. The framework provides fundamental C++ and Arduino code to interface with IMU sensors, motor encoders, LiDAR, and cameras for self-driving robots.

## **🛠 Overview**
This tutorial demonstrates how to:
- Read **IMU (MPU6050) accelerometer & gyroscope data** on an **Arduino**.
- Simulate **encoder values** for motors.
- Transmit sensor data via **serial communication** to a **Raspberry Pi (or PC)**.
- Receive and process sensor data in a **C++ application** on Raspberry Pi.

This is a **step-by-step guide** that builds the foundation for **autonomous robots** using ROS2, SLAM, and AI.

---

## **📌 Hardware Requirements**
To follow this tutorial, you will need:
1. **Raspberry Pi / PC** (Linux-based, with C++ compiler)
2. **Arduino (Uno, Mega, or Nano)**
3. **MPU6050 IMU Sensor**
4. **Motor Encoders (or Simulated Encoder Values)**
5. **USB-to-Serial connection (or direct GPIO UART for RPi)**

---

## **📂 Project Structure**
```
📁 micro-robot-framework/
│── 📜 README.md
│── 📄 microRobotFramework.hpp  # C++ Class Header
│── 📄 microRobotFramework.cpp  # C++ Implementation
│── 📄 mrf_example_01.cpp       # C++ Example Application
│── 📄 mpu6050_get_raw_data
    |── 📄 mpu6050_get_raw_data.ino          # Arduino Firmware
    |── 📄 mpu6050_get_receive_raw_data.py   # Python code for arduino code testing
```

---

## **📝 Step 1: Setting Up Arduino for IMU & Encoder Data Transmission**
### **1️⃣ Install Dependencies**
Before compiling the Arduino code, install the **MPU6050 library** in the **Arduino IDE**:
1. Open **Arduino IDE** → Go to **Library Manager** (`Sketch → Include Library → Manage Libraries`).
2. Search for `mpu6050_light` and install it.

### **2️⃣ Upload the Arduino Code**
Flash the following **Arduino code** to your board:

#### **📌 Arduino Code (`Arduino_MRF.ino`)**
```cpp
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
long timer = 0;

// Data Packet Format: [Header][Length][Sensor Data][Checksum]
byte data[23]; 

void setup() {
  Serial.begin(115200);
  Wire.begin();

  byte status = mpu.begin();
  Serial.println(status);
  pinMode(13, OUTPUT);

  while(status != 0) {  // Blink LED if IMU fails
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
  }

  Serial.println("Calibration in progress...");
  delay(1000);
  mpu.calcOffsets(true, true);
  Serial.println("IMU Ready!");
}

uint16_t encoder1 = 0, encoder2 = 0, encoder3 = 0, encoder4 = 0;

void loop() {
  mpu.update();
  if (millis() - timer > 50) {  // Send data every 50ms
    int16_t accelX = (int16_t)(mpu.getAccX() * 1000);
    int16_t accelY = (int16_t)(mpu.getAccY() * 1000);
    int16_t accelZ = (int16_t)(mpu.getAccZ() * 1000);
    int16_t gyroX = (int16_t)(mpu.getGyroX() * 1000);
    int16_t gyroY = (int16_t)(mpu.getGyroY() * 1000);
    int16_t gyroZ = (int16_t)(mpu.getGyroZ() * 1000);

    // Construct data packet
    data[0] = 0xf5; // Header
    data[1] = 21;   // Length
    data[2] = (accelX >> 8) & 0xff;
    data[3] = accelX & 0xff;
    data[4] = (accelY >> 8) & 0xff;
    data[5] = accelY & 0xff;
    data[6] = (accelZ >> 8) & 0xff;
    data[7] = accelZ & 0xff;
    data[8] = (gyroX >> 8) & 0xff;
    data[9] = gyroX & 0xff;
    data[10] = (gyroY >> 8) & 0xff;
    data[11] = gyroY & 0xff;
    data[12] = (gyroZ >> 8) & 0xff;
    data[13] = gyroZ & 0xff;
    data[14] = (encoder1 >> 8) & 0xff;
    data[15] = encoder1 & 0xff;
    data[16] = (encoder2 >> 8) & 0xff;
    data[17] = encoder2 & 0xff;
    data[18] = (encoder3 >> 8) & 0xff;
    data[19] = encoder3 & 0xff;
    data[20] = (encoder4 >> 8) & 0xff;
    data[21] = encoder4 & 0xff;
    data[22] = 0; // Checksum (Not implemented)

    Serial.write(data, 23); // Send packet
    encoder1++; encoder2++; encoder3++; encoder4++;
    timer = millis();
  }
}
```
---

## **🔹 Understanding the MRF Class (C++ API)**
The **Micro Robot Framework (MRF)** provides a structured **C++ class** to manage **sensor data reception** and **serial communication**.

### **🛠️ MRF Class Definition**
#### 📌 **File:** `microRobotFramework.hpp`
```cpp
#ifndef MRF_H
#define MRF_H

#include <string>
#include <cstdint>

class MRF {
public:
    // Constructor & Destructor
    MRF(const std::string& port, int baud_rate);  // Open Serial Connection

    // Sensor Data Reception (IMU + Encoder)
    bool receiveSensorData();  // Reads IMU & Encoder Data
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

    // Serial Communication
    bool isConnected();  // Check if Serial Connection is Active

private:
    int serial_fd;  // File Descriptor for Serial Communication
    std::string serial_port;
    int baud_rate;
    bool connected;

    // Sensor Data Storage
    int16_t accel_x, accel_y, accel_z;
    int16_t gyro_x, gyro_y, gyro_z;
    uint16_t encoder1, encoder2, encoder3, encoder4;

    // Serial Connection Helpers
    bool openSerial();  // Open Serial Connection
};

#endif // MRF_H
```

---

### **🔹 MRF Class Methods Explained**
| Method | Description |
|---------|------------|
| `MRF(const std::string& port, int baud_rate)` | Constructor. Opens the serial connection to the Arduino. |
| `bool receiveSensorData()` | Reads **IMU and encoder data** from the Arduino via serial. |
| `int16_t getAccelX(), getAccelY(), getAccelZ()` | Returns IMU accelerometer values (scaled by 1000). |
| `int16_t getGyroX(), getGyroY(), getGyroZ()` | Returns IMU gyroscope values (scaled by 1000). |
| `uint16_t getEncoder1(), getEncoder2(), getEncoder3(), getEncoder4()` | Returns simulated **motor encoder values**. |
| `bool isConnected()` | Checks if the serial connection is active. |
| `bool openSerial()` | Initializes and configures the serial port. |

---

## **📝 Step 2: Setting Up Raspberry Pi (C++ Code)**
### **1️⃣ Compile & Run the C++ Application**
```sh
g++ -o mrf_example_01 mrf_example_01.cpp microRobotFramework.cpp -std=c++11
./mrf_example_01
```

### **2️⃣ C++ Code for Receiving Sensor Data**
#### **📌 C++ Application (`mrf_example_01.cpp`)**
```cpp
#include "microRobotFramework.hpp"
#include <iostream>
#include <unistd.h>

int main() {
    MRF mrf("/dev/ttyUSB0", 115200);

    if (!mrf.isConnected()) {
        std::cout << "Serial port not connected!" << std::endl;
        return 0;
    }

    while (true) {
        if (mrf.receiveSensorData()) {
            std::cout << "AccelX: " << mrf.getAccelX() << " | "
                      << "AccelY: " << mrf.getAccelY() << " | "
                      << "AccelZ: " << mrf.getAccelZ() << std::endl;
        }
        usleep(5000);  // Delay for 5ms
    }
}
```

---

## **📌 What You Learned in This Step**
✅ **Arduino:** Reads IMU and simulated encoder values, then transmits them via serial communication.  
✅ **C++ (Raspberry Pi/PC):** Receives and processes sensor data from Arduino.  
✅ **Packet-Based Communication:** Uses a structured format for sending data between microcontrollers and SBCs.  
✅ **Serial Communication Debugging:** Ensures reliable data exchange between Arduino and Raspberry Pi.

---

## **📍 Next Steps (Step 2)**
In the next tutorial, we will:
- Implement **motor control** using **differential drive**.
- Add **motor speed control** via serial communication.
- Introduce **real-time plotting** of IMU data.

---

## **📖 References**
- [MPU6050 Light Library](https://github.com/rfetick/MPU6050_light)
- [C++ Serial Communication](https://www.cmrr.umn.edu/~strupp/serial.html)

---

