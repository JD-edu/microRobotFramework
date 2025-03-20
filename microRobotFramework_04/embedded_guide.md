# **microRobotFramework - Version 4**

## **📌 What's New in Version 4**
- **Embedded System Upgrade:** Migrated from **Arduino** to **STM32F407G-DISCO1** board.
- **Enhanced Sensor Data Transmission:**
  - STM32 firmware now sends **29-byte hex data**.
  - **Byte Array Structure:**
    1. **Accelerometer (X, Y, Z)**
    2. **Gyroscope (X, Y, Z)**
    3. **Orientation (Pitch, Roll, Yaw)**
    4. **Encoder Values (1, 2, 3, 4)**

## **📌 Features Retained from Version 3**
- **Motor Control Commands:**
  - Press `'a'` → **Motor OFF**
  - Press `'b'` → **Motor ON**

## **📌 To-Do List**
- **Implement Remaining 3 Motors** (Currently handling only 1 motor)
- **Define and Implement Motor Control Protocol**
- **Integrate ROS2 for Odometry Calculation**
  - Process encoder data for **robot localization**
  - Implement ROS2 **/odom** topic publishing


