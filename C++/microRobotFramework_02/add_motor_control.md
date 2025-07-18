---

# **Micro Robot Framework (MRF) - Step 2: Sending Motor Control Commands**

## **📌 Overview**
This is the **second step** in the **Micro Robot Framework (MRF)** tutorial series. In this tutorial, we extend the functionality from **Tutorial 1** by adding **motor control support**. Now, in addition to **receiving sensor data (IMU & encoder values)**, we can **send motor control commands** from the Raspberry Pi to the Arduino.

---

## **🔹 Changes from Tutorial 1**
| Feature | Tutorial 1 | Tutorial 2 |
|---------|-----------|-----------|
| **IMU Data Reception** | ✅ Yes | ✅ Yes |
| **Encoder Data Simulation** | ✅ Yes | ✅ Yes |
| **Motor Control Commands** | ❌ No | ✅ Yes |
| **Serial Communication** | ✅ Read-Only | ✅ Read & Write |

- **New Feature:** The Raspberry Pi can now send **speed & angle commands** to the Arduino for motor control.
- **New MRF Class Method:** `sendMotorCommand(int speed, int angle)` has been added to send motor commands.
- **Updated Arduino Code:** Added `receiveMotorCommand()` to parse motor control packets and control motors using **differential drive**.

---

## **📂 Project Structure**
```
📁 micro-robot-framework/
│── 📜 README.md
│── 📄 microRobotFramework.hpp  # C++ Class Header (MRF)
│── 📄 microRobotFramework.cpp  # C++ Implementation (MRF)
│── 📄 mrf_example_02.cpp       # C++ Example Application
│── 📁 mpu6050_get_raw_data/
│   │── 📄 mpu6050_get_raw_data.ino        # Arduino Firmware (Now with Motor Control)
│   │── 📄 mpu6050_receive_raw_data.py     # Python Code for Testing (Updated for Motors)
```

---

## **🔹 Understanding the MRF Class (C++ API)**
The **MRF class** now supports **motor control commands**.

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
    MRF(const std::string& port, int baud_rate);

    // Sensor Data Reception (IMU + Encoder)
    bool receiveSensorData();
    
    // Motor Control (New in Tutorial 2)
    bool sendMotorCommand(int speed, int angle);

    // Serial Communication
    bool isConnected();
    void closeConnection();

    // IMU Data Retrieval
    int16_t getAccelX();
    int16_t getAccelY();
    int16_t getAccelZ();
    int16_t getGyroX();
    int16_t getGyroY();
    int16_t getGyroZ();
    
    // Encoder Data Retrieval
    uint16_t getEncoder1();
    uint16_t getEncoder2();
    uint16_t getEncoder3();
    uint16_t getEncoder4();

private:
    // Serial Communication
    int serial_fd;
    std::string serial_port;
    int baud_rate;
    bool connected;

    // IMU Data
    int16_t accel_x, accel_y, accel_z;
    int16_t gyro_x, gyro_y, gyro_z;

    // Encoder Data
    uint16_t encoder1, encoder2, encoder3, encoder4;

    // Private Helpers
    bool openSerial();
};

#endif // MRF_H
```

---

## **📌 Motor Control Packet Structure**
The **motor control packet** is **5 bytes** long and follows this format:

| **Byte Index** | **Field Name** | **Description** | **Size (Bytes)** |
|--------------|--------------|----------------------------------|-------------|
| `0` | **Header** | Start-of-frame marker (`0xAA`) | 1 |
| `1` | **Length** | Fixed length (`3` for speed & angle) | 1 |
| `2` | **Speed** | Unsigned integer (`0-255`) | 1 |
| `3` | **Angle** | Signed integer (`-127 to 127`) | 1 |
| `4` | **Checksum** | XOR of all previous bytes | 1 |

### **Example Packet (Hex Representation)**
| Byte | Value (Example) | Description |
|------|---------------|-------------|
| `0` | `0xAA` | Header |
| `1` | `0x03` | Length = `3` (Speed + Angle + Checksum) |
| `2` | `0x64` | Speed = `100` (out of 255) |
| `3` | `0x10` | Angle = `16` |
| `4` | `CD` | Checksum (`0xAA ^ 0x03 ^ 0x64 ^ 0x10`) |

---

## **📝 Step 1: Setting Up Arduino - Sensor & Motor Control**
The Arduino now:
- **Receives motor control commands** (`speed` & `angle`).
- **Controls motors using differential drive logic**.
- **Sends IMU & encoder data (same as Tutorial 1).**

#### **📌 Arduino Code (`mpu6050_get_raw_data.ino`)**
```cpp
#include "Wire.h"
#include <MPU6050_light.h>
#include <SoftwareSerial.h>

#define RX_PIN 7   // Arduino RX
#define TX_PIN 8   // Arduino TX

#define LEFT_MOTOR_PWM 5
#define LEFT_MOTOR_DIR 4
#define RIGHT_MOTOR_PWM 6
#define RIGHT_MOTOR_DIR 7

SoftwareSerial softSerial(RX_PIN, TX_PIN);
MPU6050 mpu(Wire);
long timer = 0;
byte data[23]; 

void setup() {
  Serial.begin(115200);
  softSerial.begin(9600);
  Wire.begin();
  softSerial.println("Motor simulation...");
  
  byte status = mpu.begin();
  Serial.println(status);
  
  pinMode(LEFT_MOTOR_PWM, OUTPUT);
  pinMode(LEFT_MOTOR_DIR, OUTPUT);
  pinMode(RIGHT_MOTOR_PWM, OUTPUT);
  pinMode(RIGHT_MOTOR_DIR, OUTPUT);
}

void loop() {
  mpu.update();
  receiveMotorCommand();
}

// Receive & Process Motor Commands
void receiveMotorCommand() {
  if (Serial.available() >= 5) {
    uint8_t packet[5];
    Serial.readBytes(packet, 5);

    if (packet[0] != 0xAA) return;

    int speed = packet[2];
    int angle = (int8_t)packet[3];

    int left_speed = constrain(speed - (angle / 127.0) * speed, -255, 255);
    int right_speed = constrain(speed + (angle / 127.0) * speed, -255, 255);

    controlMotors(left_speed, right_speed);
  }
}

void controlMotors(int left_speed, int right_speed) {
  if (left_speed > 0) {
    analogWrite(LEFT_MOTOR_PWM, left_speed);
    digitalWrite(LEFT_MOTOR_DIR, HIGH);
  } else {
    analogWrite(LEFT_MOTOR_PWM, -left_speed);
    digitalWrite(LEFT_MOTOR_DIR, LOW);
  }

  if (right_speed > 0) {
    analogWrite(RIGHT_MOTOR_PWM, right_speed);
    digitalWrite(RIGHT_MOTOR_DIR, HIGH);
  } else {
    analogWrite(RIGHT_MOTOR_PWM, -right_speed);
    digitalWrite(RIGHT_MOTOR_DIR, LOW);
  }
}
```

---

## **📍 Next Steps (Step 3)**
- Implement **closed-loop PID control** for smoother motor control.
- Add **real-time visualization** for IMU & encoder data.
- Implement **two-way communication** for sensor data acknowledgment.

---

## **📖 References**
- [MPU6050 Light Library](https://github.com/rfetick/MPU6050_light)
- [C++ Serial Communication](https://www.cmrr.umn.edu/~strupp/serial.html)

---

🚀 **Now You're Ready to Move to the Next Step!** 🚀  

Would you like to add **live data visualization** for motor response in **Step 3**? 📊🔥
