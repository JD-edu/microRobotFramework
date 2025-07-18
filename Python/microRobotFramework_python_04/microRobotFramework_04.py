"""
microRobotFramework_04.py
Python version of the microRobotFramework C++ class for 2-wheel robot control
Converted from microRobotFramework.hpp and microRobotFramework.cpp (version 04)
Includes enhanced motor control with speed and angle parameters
"""

import serial
import struct
import time
import math
from typing import Optional, Tuple

class MRF:
    """
    MicroRobotFramework class for 2-wheel robot control (Version 04)
    Handles serial communication, sensor data reception (IMU + Encoder), and motor control
    Enhanced with speed and angle-based motor control
    """

    # Constants
    HEADER_BYTE = 0xF5  # Header byte for serial communication

    def __init__(self, port: str, baud_rate: int):
        """
        Constructor

        Args:
            port (str): Serial port path (e.g., '/dev/ttyACM0')
            baud_rate (int): Baud rate for serial communication (e.g., 115200)
        """
        self.serial_port = port
        self.baud_rate = baud_rate
        self.connected = False
        self.serial_connection: Optional[serial.Serial] = None

        # IMU Data
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0

        # Encoder Data
        self.encoder1 = 0
        self.encoder2 = 0
        self.encoder3 = 0
        self.encoder4 = 0

        # Initialize serial connection
        self.connected = self._open_serial()

    def _open_serial(self) -> bool:
        """
        Open serial connection

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.serial_connection = serial.Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=0.1,  # 100ms timeout
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            return True
        except (serial.SerialException, OSError) as e:
            print(f"Error opening serial port {self.serial_port}: {e}")
            return False

    def is_connected(self) -> bool:
        """
        Check if serial connection is active

        Returns:
            bool: True if connected, False otherwise
        """
        return self.connected and self.serial_connection is not None and self.serial_connection.is_open

    def receive_sensor_data(self) -> bool:
        """
        Receive sensor data from serial port (IMU + Encoder data)
        Reads 23 bytes total: header + 22 data bytes

        Returns:
            bool: True if data received successfully, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            # Read 23 bytes of data
            buffer = self.serial_connection.read(23)
            if len(buffer) != 23:
                return False  # Incomplete packet

            # Parse the data (assuming big-endian format based on C++ code)
            # Skip first 2 bytes (header), then parse sensor data
            self.accel_x = (buffer[2] << 8) | buffer[3]
            self.accel_y = (buffer[4] << 8) | buffer[5]
            self.accel_z = (buffer[6] << 8) | buffer[7]
            self.gyro_x = (buffer[8] << 8) | buffer[9]
            self.gyro_y = (buffer[10] << 8) | buffer[11]
            self.gyro_z = (buffer[12] << 8) | buffer[13]
            self.encoder1 = (buffer[14] << 8) | buffer[15]
            self.encoder2 = (buffer[16] << 8) | buffer[17]
            self.encoder3 = (buffer[18] << 8) | buffer[19]
            self.encoder4 = (buffer[20] << 8) | buffer[21]

            # Convert to signed integers for IMU data
            if self.accel_x > 32767:
                self.accel_x -= 65536
            if self.accel_y > 32767:
                self.accel_y -= 65536
            if self.accel_z > 32767:
                self.accel_z -= 65536
            if self.gyro_x > 32767:
                self.gyro_x -= 65536
            if self.gyro_y > 32767:
                self.gyro_y -= 65536
            if self.gyro_z > 32767:
                self.gyro_z -= 65536

            return True

        except (serial.SerialException, OSError) as e:
            print(f"Error reading serial data: {e}")
            return False

    def send_motor_command(self, speed: int, angle: int) -> bool:
        """
        Send motor control commands to the robot (Version 04 enhanced)

        Args:
            speed (int): Motor speed (-100 to +100)
            angle (int): Steering angle (-100 to +100, 0 = straight)

        Returns:
            bool: True if command sent successfully, False otherwise
        """
        if not self.is_connected():
            return False

        # Validate input ranges
        speed = max(-100, min(100, speed))
        angle = max(-100, min(100, angle))

        # Convert speed and angle to left/right motor speeds
        left_speed, right_speed = self._calculate_differential_speeds(speed, angle)

        try:
            # Create motor command packet (assuming similar format to previous versions)
            # Header byte + left speed + right speed
            command = struct.pack('<Bhh', 0xFA, left_speed, right_speed)

            self.serial_connection.write(command)
            return True

        except (serial.SerialException, OSError) as e:
            print(f"Error sending motor command: {e}")
            return False

    def _calculate_differential_speeds(self, speed: int, angle: int) -> Tuple[int, int]:
        """
        Calculate left and right motor speeds from speed and angle

        Args:
            speed (int): Forward/backward speed (-100 to +100)
            angle (int): Steering angle (-100 to +100)

        Returns:
            Tuple[int, int]: (left_speed, right_speed)
        """
        # Convert angle to differential factor
        angle_factor = angle / 100.0  # Normalize to -1.0 to +1.0

        if angle_factor >= 0:  # Turn right
            left_speed = speed
            right_speed = int(speed * (1.0 - angle_factor))
        else:  # Turn left
            left_speed = int(speed * (1.0 + angle_factor))
            right_speed = speed

        return left_speed, right_speed

    # Convenience methods for common movements
    def move_forward(self, speed: int = 50) -> bool:
        """Move robot forward"""
        return self.send_motor_command(speed, 0)

    def move_backward(self, speed: int = 50) -> bool:
        """Move robot backward"""
        return self.send_motor_command(-speed, 0)

    def turn_left(self, speed: int = 50, angle: int = 50) -> bool:
        """Turn robot left"""
        return self.send_motor_command(speed, -angle)

    def turn_right(self, speed: int = 50, angle: int = 50) -> bool:
        """Turn robot right"""
        return self.send_motor_command(speed, angle)

    def stop_motors(self) -> bool:
        """Stop both motors"""
        return self.send_motor_command(0, 0)

    # Getter methods for IMU data
    def get_accel_x(self) -> int:
        """Get X-axis acceleration"""
        return self.accel_x

    def get_accel_y(self) -> int:
        """Get Y-axis acceleration"""
        return self.accel_y

    def get_accel_z(self) -> int:
        """Get Z-axis acceleration"""
        return self.accel_z

    def get_gyro_x(self) -> int:
        """Get X-axis gyroscope data"""
        return self.gyro_x

    def get_gyro_y(self) -> int:
        """Get Y-axis gyroscope data"""
        return self.gyro_y

    def get_gyro_z(self) -> int:
        """Get Z-axis gyroscope data"""
        return self.gyro_z

    # Getter methods for Encoder data
    def get_encoder1(self) -> int:
        """Get encoder 1 value"""
        return self.encoder1

    def get_encoder2(self) -> int:
        """Get encoder 2 value"""
        return self.encoder2

    def get_encoder3(self) -> int:
        """Get encoder 3 value"""
        return self.encoder3

    def get_encoder4(self) -> int:
        """Get encoder 4 value"""
        return self.encoder4

    def get_all_sensor_data(self) -> dict:
        """Get all sensor data as dictionary"""
        return {
            'accel': {'x': self.accel_x, 'y': self.accel_y, 'z': self.accel_z},
            'gyro': {'x': self.gyro_x, 'y': self.gyro_y, 'z': self.gyro_z},
            'encoders': {
                'encoder1': self.encoder1,
                'encoder2': self.encoder2,
                'encoder3': self.encoder3,
                'encoder4': self.encoder4
            }
        }

    def close_connection(self) -> None:
        """Close serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.connected = False

    def __del__(self):
        """Destructor - ensure serial connection is closed"""
        self.close_connection()
