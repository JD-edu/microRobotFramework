#!/usr/bin/env python3
"""
mrf_example_01.py
Python version of the microRobotFramework example
Converted from mrf_example_01.cpp

This example demonstrates basic usage of the MRF class:
- Connect to serial port
- Continuously read sensor data (IMU + Encoder)
- Display accelerometer data

Usage:
    python3 mrf_example_01.py
"""

import time
import sys
from microRobotFramework import MRF


def main():
    """
    Main function - equivalent to C++ main()
    """
    # Initialize MRF with serial port and baud rate
    # Note: You may need to change '/dev/ttyACM0' to your actual serial port
    # On Windows, it might be 'COM3', 'COM4', etc.
    # On Linux/macOS, it might be '/dev/ttyUSB0', '/dev/ttyACM0', etc.
    mrf = MRF("COM5", 115200)

    # Check if serial connection is established
    if not mrf.is_connected():
        print("Serial port is not connected")
        print("Please check:")
        print("1. Serial port path (e.g., /dev/ttyACM0, COM3)")
        print("2. Device is connected and powered on")
        print("3. Correct permissions for serial port access")
        return 1

    print("✅ Serial connection established!")
    print("📡 Starting sensor data reception...")
    print("Press Ctrl+C to stop")
    print("-" * 50)

    try:
        # Main loop - equivalent to C++ while(true) loop
        while True:
            # Receive sensor data
            ret = mrf.receive_sensor_data()

            if ret:
                # Display accelerometer data (same as C++ example)
                accel_x = mrf.get_accel_x()
                accel_y = mrf.get_accel_y()
                accel_z = mrf.get_accel_z()

                print(f"{accel_x:6d}  {accel_y:6d}  {accel_z:6d}")

                # Optional: Display additional sensor data
                # Uncomment the following lines to see gyroscope and encoder data
                """
                gyro_x = mrf.get_gyro_x()
                gyro_y = mrf.get_gyro_y()
                gyro_z = mrf.get_gyro_z()

                enc1 = mrf.get_encoder1()
                enc2 = mrf.get_encoder2()
                enc3 = mrf.get_encoder3()
                enc4 = mrf.get_encoder4()

                print(f"Accel: ({accel_x:6d}, {accel_y:6d}, {accel_z:6d})")
                print(f"Gyro:  ({gyro_x:6d}, {gyro_y:6d}, {gyro_z:6d})")
                print(f"Enc:   ({enc1:5d}, {enc2:5d}, {enc3:5d}, {enc4:5d})")
                print("-" * 50)
                """

            # Sleep for 5ms (equivalent to C++ usleep(5000))
            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return 1
    finally:
        # Clean up - close serial connection
        mrf.close_connection()
        print("🔌 Serial connection closed")

    return 0


if __name__ == "__main__":
    """
    Entry point - equivalent to C++ main() function
    """
    exit_code = main()
    sys.exit(exit_code)
