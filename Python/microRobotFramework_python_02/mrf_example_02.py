#!/usr/bin/env python3
"""
mrf_example_02.py
Python version of the microRobotFramework example with motor control
Converted from mrf_example_02.cpp

This example demonstrates:
- Connect to serial port
- Continuously read sensor data (IMU + Encoder)
- Display accelerometer data
- Send motor control commands periodically (every 100 sensor readings)
- Prevent serial buffer overflow with proper timing

Usage:
    python3 mrf_example_02.py
"""

import time
import sys
from microRobotFramework_02 import MRF


def main():
    """
    Main function - equivalent to C++ main()
    """
    count = 0
    ret = False

    # Initialize MRF with serial port and baud rate
    # Note: You may need to change '/dev/ttyACM0' to your actual serial port
    # On Windows, it might be 'COM3', 'COM4', etc.
    # On Linux/macOS, it might be '/dev/ttyUSB0', '/dev/ttyACM0', etc.
    mrf = MRF("/dev/ttyACM0", 115200)

    # Check if serial connection is established
    if not mrf.is_connected():
        print("Serial port is not connected")
        print("Please check:")
        print("1. Serial port path (e.g., /dev/ttyACM0, COM3)")
        print("2. Device is connected and powered on")
        print("3. Correct permissions for serial port access")
        return 1

    print("✅ Serial connection established!")
    print("📡 Starting sensor data reception with motor control...")
    print("🎮 Motor commands will be sent every 100 sensor readings")
    print("Press Ctrl+C to stop")
    print("-" * 60)

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

            # Sleep for 1ms (equivalent to C++ usleep(1000))
            time.sleep(0.001)

            # Motor control logic - equivalent to C++ cooling down mechanism
            """
            Cooling down. If we send motor command with short interval, 
            Arduino serial buffer is freezed. 
            Below code is just study and test purpose only. 
            Use thread to receiving IMU and send motor command at same time 
            """
            if count > 100:
                # Send motor command: speed=90, angle=100
                motor_success = mrf.send_motor_command(90, 100)
                if motor_success:
                    print(f"🎮 Motor command sent: speed=90, angle=100")
                else:
                    print("❌ Failed to send motor command")
                count = 0
            else:
                count += 1

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


def advanced_example():
    """
    Advanced example with separate motor control patterns
    This demonstrates more sophisticated motor control
    """
    mrf = MRF("/dev/ttyACM0", 115200)

    if not mrf.is_connected():
        print("Serial port is not connected")
        return 1

    print("🚀 Advanced motor control example")
    print("This will demonstrate various movement patterns")

    try:
        sensor_count = 0
        motor_pattern = 0

        while True:
            # Read sensor data
            if mrf.receive_sensor_data():
                accel_x = mrf.get_accel_x()
                accel_y = mrf.get_accel_y()
                accel_z = mrf.get_accel_z()

                # Display sensor data less frequently to reduce output
                if sensor_count % 50 == 0:
                    print(f"Sensors: X={accel_x:6d}, Y={accel_y:6d}, Z={accel_z:6d}")

            time.sleep(0.001)
            sensor_count += 1

            # Send different motor commands every 100 readings
            if sensor_count > 100:
                if motor_pattern == 0:
                    # Move forward
                    mrf.send_motor_command(100, 0)
                    print("🎮 Moving forward")
                elif motor_pattern == 1:
                    # Turn right
                    mrf.send_motor_command(80, 45)
                    print("🎮 Turning right")
                elif motor_pattern == 2:
                    # Move backward
                    mrf.send_motor_command(-80, 0)
                    print("🎮 Moving backward")
                elif motor_pattern == 3:
                    # Turn left
                    mrf.send_motor_command(80, -45)
                    print("🎮 Turning left")
                elif motor_pattern == 4:
                    # Stop
                    mrf.send_motor_command(0, 0)
                    print("🎮 Stopping")

                motor_pattern = (motor_pattern + 1) % 5
                sensor_count = 0

    except KeyboardInterrupt:
        print("\n🛑 Advanced example interrupted")
    finally:
        mrf.close_connection()
        print("🔌 Connection closed")

    return 0


if __name__ == "__main__":
    """
    Entry point - equivalent to C++ main() function
    """
    import argparse

    parser = argparse.ArgumentParser(description='MicroRobotFramework Example 02')
    parser.add_argument('--advanced', action='store_true', 
                       help='Run advanced motor control example')

    args = parser.parse_args()

    if args.advanced:
        exit_code = advanced_example()
    else:
        exit_code = main()

    sys.exit(exit_code)
