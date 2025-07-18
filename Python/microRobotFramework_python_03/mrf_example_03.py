#!/usr/bin/env python3
"""
mrf_example_03.py
Python version of the microRobotFramework example with multi-threading support
Converted from mrf_example_03.cpp

This example demonstrates:
- Multi-threading for concurrent sensor reading and motor control
- Thread-safe serial communication using mutex
- Real-time sensor data display
- Continuous motor command sending
- Graceful thread shutdown

Usage:
    python3 mrf_example_03.py
"""

import time
import sys
import threading
import signal
from microRobotFramework_03 import MRF, MRFThreadManager


class MRFExample03:
    """
    Example application demonstrating multi-threading capabilities
    """

    def __init__(self, port: str = "/dev/ttyUSB0", baud_rate: int = 115200):
        """
        Initialize the example application

        Args:
            port (str): Serial port path
            baud_rate (int): Serial communication baud rate
        """
        self.mrf = MRF(port, baud_rate)
        self.thread_manager = MRFThreadManager(self.mrf)
        self.running = True

        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C signal for graceful shutdown"""
        print("
🛑 Received interrupt signal. Shutting down gracefully...")
        self.running = False

    def run_basic_example(self):
        """
        Run basic multi-threading example
        Equivalent to the C++ main() function
        """
        print("🤖 microRobotFramework Version 03 - Multi-threading Example")
        print("=" * 60)

        # Check serial connection
        if not self.mrf.is_connected():
            print("❌ Serial port is not connected")
            print("Please check:")
            print("1. Serial port path (e.g., /dev/ttyUSB0, COM3)")
            print("2. Device is connected and powered on")
            print("3. Correct permissions for serial port access")
            return 1

        print("✅ Serial connection established!")
        print("🧵 Starting multi-threading operations...")
        print("📡 Sensor data reading thread: 50ms interval")
        print("🎮 Motor command thread: 100ms interval")
        print("Press ENTER to stop or Ctrl+C for immediate shutdown")
        print("-" * 60)

        try:
            # Start sensor reading thread (50ms interval)
            self.thread_manager.start_sensor_thread(read_interval=0.05)

            # Start motor command thread (speed=90, angle=100, 100ms interval)
            self.thread_manager.start_motor_thread(
                speed=90, 
                angle=100, 
                command_interval=0.1
            )

            # Main thread - display sensor data
            self._display_sensor_data()

        except KeyboardInterrupt:
            print("
🛑 Program interrupted by user")
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            return 1
        finally:
            self._cleanup()

        return 0

    def _display_sensor_data(self):
        """
        Display sensor data in main thread
        """
        last_display_time = time.time()
        display_interval = 0.2  # Display every 200ms

        print("📊 Real-time Sensor Data (Press ENTER to stop):")
        print("AccelX    AccelY    AccelZ    GyroX     GyroY     GyroZ")
        print("-" * 60)

        # Non-blocking input setup
        import select
        import sys

        while self.running and self.mrf.running.is_set():
            current_time = time.time()

            # Display sensor data at specified interval
            if current_time - last_display_time >= display_interval:
                accel_x = self.mrf.get_accel_x()
                accel_y = self.mrf.get_accel_y()
                accel_z = self.mrf.get_accel_z()
                gyro_x = self.mrf.get_gyro_x()
                gyro_y = self.mrf.get_gyro_y()
                gyro_z = self.mrf.get_gyro_z()

                print(f"{accel_x:6d}    {accel_y:6d}    {accel_z:6d}    "
                      f"{gyro_x:6d}    {gyro_y:6d}    {gyro_z:6d}")

                last_display_time = current_time

            # Check for user input (non-blocking on Unix systems)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input()  # Consume the input
                break

            time.sleep(0.01)  # Small sleep to prevent busy waiting

    def _cleanup(self):
        """
        Clean up resources and stop threads
        """
        print("
🧹 Cleaning up...")

        # Stop all threads
        self.thread_manager.stop_all_threads()

        # Close serial connection
        self.mrf.close_connection()

        print("🔌 Serial connection closed")
        print("✅ Cleanup completed")

    def run_advanced_example(self):
        """
        Run advanced example with custom motor control patterns
        """
        print("🤖 microRobotFramework Version 03 - Advanced Multi-threading Example")
        print("=" * 70)

        if not self.mrf.is_connected():
            print("❌ Serial port is not connected")
            return 1

        print("✅ Serial connection established!")
        print("🎯 Running advanced motor control patterns...")
        print("Press Ctrl+C to stop")
        print("-" * 70)

        try:
            # Start sensor reading thread
            self.thread_manager.start_sensor_thread(read_interval=0.05)

            # Run motor control patterns
            self._run_motor_patterns()

        except KeyboardInterrupt:
            print("
🛑 Program interrupted by user")
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            return 1
        finally:
            self._cleanup()

        return 0

    def _run_motor_patterns(self):
        """
        Run different motor control patterns
        """
        patterns = [
            {"name": "Forward", "speed": 100, "angle": 0, "duration": 3},
            {"name": "Turn Right", "speed": 80, "angle": 50, "duration": 2},
            {"name": "Turn Left", "speed": 80, "angle": -50, "duration": 2},
            {"name": "Backward", "speed": 60, "angle": 0, "duration": 2},
            {"name": "Stop", "speed": 0, "angle": 0, "duration": 1},
        ]

        for pattern in patterns:
            if not self.running or not self.mrf.running.is_set():
                break

            print(f"🎮 Pattern: {pattern['name']} "
                  f"(Speed={pattern['speed']}, Angle={pattern['angle']}) "
                  f"for {pattern['duration']}s")

            # Send motor commands for the pattern duration
            start_time = time.time()
            while (time.time() - start_time) < pattern['duration']:
                if not self.running or not self.mrf.running.is_set():
                    break

                self.mrf.send_motor_command(pattern['speed'], pattern['angle'])

                # Display sensor data
                accel_x = self.mrf.get_accel_x()
                accel_y = self.mrf.get_accel_y()
                accel_z = self.mrf.get_accel_z()
                print(f"  📊 Accel: X={accel_x:6d}, Y={accel_y:6d}, Z={accel_z:6d}")

                time.sleep(0.1)  # 100ms interval

        print("🏁 Motor pattern sequence completed")


def main():
    """
    Main function - equivalent to C++ main()
    """
    print("🚀 Starting microRobotFramework Version 03 Example")

    # You may need to change the serial port for your system:
    # Linux/macOS: '/dev/ttyUSB0', '/dev/ttyACM0'
    # Windows: 'COM3', 'COM4', etc.
    example = MRFExample03("/dev/ttyUSB0", 115200)

    # Choose example type
    print("
Select example type:")
    print("1. Basic multi-threading example (default)")
    print("2. Advanced motor control patterns")

    try:
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "2":
            exit_code = example.run_advanced_example()
        else:
            exit_code = example.run_basic_example()

        return exit_code

    except KeyboardInterrupt:
        print("
🛑 Program interrupted during setup")
        return 1
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return 1


if __name__ == "__main__":
    """
    Entry point - equivalent to C++ main() function
    """
    exit_code = main()
    sys.exit(exit_code)
