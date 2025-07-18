#!/usr/bin/env python3
"""
mrf_example_04.py
Python version of the microRobotFramework example with odometry
Converted from C++ version 04

This example demonstrates:
- Basic robot control with enhanced motor commands (speed + angle)
- Sensor data reception (IMU + Encoder)
- Odometry calculations and position tracking
- Real-time monitoring and logging

Usage:
    python3 mrf_example_04.py
"""

import time
import sys
import json
import threading
from datetime import datetime
from microRobotFramework_04 import MRF
from MRF_odometry import MRF_Odometry

class RobotController:
    """
    Main robot controller class that integrates MRF and odometry
    """

    def __init__(self, port: str = "/dev/ttyACM0", baud_rate: int = 115200):
        """
        Initialize robot controller

        Args:
            port (str): Serial port path
            baud_rate (int): Serial communication baud rate
        """
        self.mrf = MRF(port, baud_rate)
        self.odometry = MRF_Odometry(
            wheel_base=0.2,      # 20cm wheel base
            wheel_radius=0.05,   # 5cm wheel radius
            encoder_resolution=1024  # 1024 pulses per revolution
        )

        self.running = False
        self.data_log = []
        self.log_interval = 0.1  # Log data every 100ms

    def start_monitoring(self):
        """Start sensor monitoring and odometry updates"""
        self.running = True
        print("🚀 Starting robot monitoring...")
        print("📡 Sensor data reception active")
        print("📍 Odometry tracking enabled")
        print("Press Ctrl+C to stop")
        print("-" * 60)

        try:
            last_log_time = time.time()

            while self.running:
                # Receive sensor data
                if self.mrf.receive_sensor_data():
                    # Update odometry with encoder data
                    encoder_left = self.mrf.get_encoder1()  # Assuming encoder1 is left wheel
                    encoder_right = self.mrf.get_encoder2()  # Assuming encoder2 is right wheel

                    self.odometry.update_odometry(encoder_left, encoder_right)

                    # Log data periodically
                    current_time = time.time()
                    if current_time - last_log_time >= self.log_interval:
                        self._log_data()
                        self._display_status()
                        last_log_time = current_time

                time.sleep(0.01)  # 10ms loop

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
        finally:
            self.stop_monitoring()

    def _log_data(self):
        """Log current sensor and odometry data"""
        timestamp = time.time()

        # Get all sensor data
        sensor_data = self.mrf.get_all_sensor_data()

        # Get odometry data
        position = self.odometry.get_position_dict()
        velocity = self.odometry.get_velocity_dict()

        # Create log entry
        log_entry = {
            'timestamp': timestamp,
            'datetime': datetime.fromtimestamp(timestamp).isoformat(),
            'sensors': sensor_data,
            'position': position,
            'velocity': velocity
        }

        self.data_log.append(log_entry)

        # Limit log size to prevent memory issues
        if len(self.data_log) > 1000:
            self.data_log.pop(0)

    def _display_status(self):
        """Display current robot status"""
        # Get current data
        accel_x = self.mrf.get_accel_x()
        accel_y = self.mrf.get_accel_y()
        accel_z = self.mrf.get_accel_z()

        gyro_x = self.mrf.get_gyro_x()
        gyro_y = self.mrf.get_gyro_y()
        gyro_z = self.mrf.get_gyro_z()

        enc1 = self.mrf.get_encoder1()
        enc2 = self.mrf.get_encoder2()

        position = self.odometry.get_position()
        velocity = self.odometry.get_velocity()

        # Display formatted data
        print(f"🔄 IMU    - Accel: ({accel_x:6d}, {accel_y:6d}, {accel_z:6d}) "
              f"Gyro: ({gyro_x:6d}, {gyro_y:6d}, {gyro_z:6d})")
        print(f"⚙️  ENC    - Left: {enc1:6d}  Right: {enc2:6d}")
        print(f"📍 POS    - X: {position.x:7.3f}m  Y: {position.y:7.3f}m  θ: {position.theta*180/3.14159:6.1f}°")
        print(f"🏃 VEL    - Linear: {velocity.linear:6.3f}m/s  Angular: {velocity.angular*180/3.14159:6.1f}°/s")
        print("-" * 60)

    def stop_monitoring(self):
        """Stop monitoring and cleanup"""
        self.running = False
        self.mrf.stop_motors()
        print("🔌 Closing connections...")
        self.mrf.close_connection()

    def run_basic_movement_demo(self):
        """Run basic movement demonstration"""
        print("🎮 Starting basic movement demo...")

        movements = [
            ("Forward", lambda: self.mrf.move_forward(50), 2.0),
            ("Stop", lambda: self.mrf.stop_motors(), 1.0),
            ("Turn Right", lambda: self.mrf.turn_right(40, 60), 2.0),
            ("Stop", lambda: self.mrf.stop_motors(), 1.0),
            ("Backward", lambda: self.mrf.move_backward(50), 2.0),
            ("Stop", lambda: self.mrf.stop_motors(), 1.0),
            ("Turn Left", lambda: self.mrf.turn_left(40, 60), 2.0),
            ("Stop", lambda: self.mrf.stop_motors(), 1.0),
        ]

        for movement_name, movement_func, duration in movements:
            print(f"🎯 {movement_name}...")
            movement_func()

            # Monitor during movement
            start_time = time.time()
            while time.time() - start_time < duration:
                if self.mrf.receive_sensor_data():
                    encoder_left = self.mrf.get_encoder1()
                    encoder_right = self.mrf.get_encoder2()
                    self.odometry.update_odometry(encoder_left, encoder_right)
                time.sleep(0.05)

        print("✅ Movement demo completed!")

        # Display final statistics
        stats = self.odometry.get_statistics()
        print("\n📊 Final Statistics:")
        print(f"   Total distance: {stats['total_distance']:.3f}m")
        print(f"   Total rotation: {stats['total_rotation_degrees']:.1f}°")
        print(f"   Path points: {stats['path_points']}")

    def run_square_pattern(self):
        """Run square movement pattern"""
        print("🔲 Starting square pattern demo...")

        # Reset odometry for clean start
        self.odometry.reset_odometry()

        # Square pattern: forward -> turn right -> repeat 4 times
        for i in range(4):
            print(f"🎯 Side {i+1}/4: Moving forward...")
            self.mrf.move_forward(60)

            # Move forward for 3 seconds while monitoring
            start_time = time.time()
            while time.time() - start_time < 3.0:
                if self.mrf.receive_sensor_data():
                    encoder_left = self.mrf.get_encoder1()
                    encoder_right = self.mrf.get_encoder2()
                    self.odometry.update_odometry(encoder_left, encoder_right)
                time.sleep(0.05)

            print(f"🎯 Corner {i+1}/4: Turning right...")
            self.mrf.turn_right(50, 80)

            # Turn for 1.5 seconds
            start_time = time.time()
            while time.time() - start_time < 1.5:
                if self.mrf.receive_sensor_data():
                    encoder_left = self.mrf.get_encoder1()
                    encoder_right = self.mrf.get_encoder2()
                    self.odometry.update_odometry(encoder_left, encoder_right)
                time.sleep(0.05)

        # Stop motors
        self.mrf.stop_motors()
        print("✅ Square pattern completed!")

        # Display final position
        final_pos = self.odometry.get_position()
        print(f"📍 Final position: ({final_pos.x:.3f}, {final_pos.y:.3f}, {final_pos.theta*180/3.14159:.1f}°)")

        # Calculate distance from origin
        distance_from_origin = self.odometry.calculate_distance_to_point(0, 0)
        print(f"📏 Distance from origin: {distance_from_origin:.3f}m")

    def save_log_data(self, filename: str = None):
        """Save logged data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/home/user/output/robot_log_{timestamp}.json"

        try:
            # Add odometry statistics to log
            log_data = {
                'metadata': {
                    'total_entries': len(self.data_log),
                    'recording_duration': self.data_log[-1]['timestamp'] - self.data_log[0]['timestamp'] if self.data_log else 0,
                    'odometry_stats': self.odometry.get_statistics(),
                    'path_history': self.odometry.export_path_to_dict()
                },
                'data': self.data_log
            }

            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2)

            print(f"💾 Log data saved to: {filename}")
            print(f"📊 Total entries: {len(self.data_log)}")

        except Exception as e:
            print(f"❌ Error saving log data: {e}")


def main():
    """
    Main function - equivalent to C++ main()
    """
    print("🤖 microRobotFramework_04 Python Example")
    print("=" * 50)

    # Initialize robot controller
    # Note: Change '/dev/ttyACM0' to your actual serial port
    # On Windows: 'COM3', 'COM4', etc.
    # On Linux/macOS: '/dev/ttyUSB0', '/dev/ttyACM0', etc.
    robot = RobotController("/dev/ttyACM0", 115200)

    # Check connection
    if not robot.mrf.is_connected():
        print("❌ Serial port is not connected")
        print("Please check:")
        print("1. Serial port path (e.g., /dev/ttyACM0, COM3)")
        print("2. Device is connected and powered on")
        print("3. Correct permissions for serial port access")
        return 1

    print("✅ Serial connection established!")
    print("🔧 Robot controller initialized")

    # Menu system
    while True:
        print("\n🎮 Select operation:")
        print("1. Real-time monitoring")
        print("2. Basic movement demo")
        print("3. Square pattern demo")
        print("4. Save log data")
        print("5. Reset odometry")
        print("6. Show statistics")
        print("0. Exit")

        try:
            choice = input("Enter choice (0-6): ").strip()

            if choice == '0':
                break
            elif choice == '1':
                robot.start_monitoring()
            elif choice == '2':
                robot.run_basic_movement_demo()
            elif choice == '3':
                robot.run_square_pattern()
            elif choice == '4':
                robot.save_log_data()
            elif choice == '5':
                robot.odometry.reset_odometry()
            elif choice == '6':
                stats = robot.odometry.get_statistics()
                print("\n📊 Current Statistics:")
                for key, value in stats.items():
                    if isinstance(value, dict):
                        print(f"   {key}:")
                        for sub_key, sub_value in value.items():
                            print(f"     {sub_key}: {sub_value}")
                    else:
                        print(f"   {key}: {value}")
            else:
                print("❌ Invalid choice. Please try again.")

        except KeyboardInterrupt:
            print("\n🛑 Program interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

    # Cleanup
    robot.stop_monitoring()
    print("👋 Program terminated")
    return 0


if __name__ == "__main__":
    """
    Entry point - equivalent to C++ main() function
    """
    exit_code = main()
    sys.exit(exit_code)
