"""
microRobotFramework_02.py
Python version of the microRobotFramework C++ class for 2-wheel robot control
Version 2: Added motor control functionality
Converted from microRobotFramework_02.hpp and microRobotFramework_02.cpp
"""

import serial
import struct
import time
import errno
from typing import Optional, Tuple

class MRF:
    """
    MicroRobotFramework class for 2-wheel robot control
    Version 2: Handles serial communication, sensor data reception (IMU + Encoder) and motor control
    """

    # Constants
    HEADER_BYTE = 0xF5  # Header byte for sensor data reception
    MOTOR_HEADER_BYTE = 0xFA  # Header byte for motor control commands

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
        Reads 21 bytes total: 1 header byte (0xF5) + 20 data bytes

        Returns:
            bool: True if data received successfully, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            # 1. Find header byte (0xF5)
            while True:
                header_byte = self.serial_connection.read(1)
                if len(header_byte) == 0:  # Timeout
                    return False

                if header_byte[0] == self.HEADER_BYTE:
                    break  # Header found

            # 2. Read remaining 20 bytes of data
            data_buffer = self.serial_connection.read(20)
            if len(data_buffer) != 20:
                return False  # Incomplete packet

            # 3. Parse the data
            self._parse_sensor_data(data_buffer)
            return True

        except (serial.SerialException, OSError) as e:
            print(f"Error reading serial data: {e}")
            return False

    def _parse_sensor_data(self, data_buffer: bytes) -> None:
        """
        Parse sensor data from buffer
        Data format: 6 int16 values (IMU) + 4 uint16 values (Encoders)

        Args:
            data_buffer (bytes): 20-byte data buffer
        """
        try:
            # Unpack data: 6 signed 16-bit integers + 4 unsigned 16-bit integers
            # '<' means little-endian format
            unpacked_data = struct.unpack('<6h4H', data_buffer)

            # IMU data (first 6 values)
            self.accel_x = unpacked_data[0]
            self.accel_y = unpacked_data[1] 
            self.accel_z = unpacked_data[2]
            self.gyro_x = unpacked_data[3]
            self.gyro_y = unpacked_data[4]
            self.gyro_z = unpacked_data[5]

            # Encoder data (last 4 values)
            self.encoder1 = unpacked_data[6]
            self.encoder2 = unpacked_data[7]
            self.encoder3 = unpacked_data[8]
            self.encoder4 = unpacked_data[9]

        except struct.error as e:
            print(f"Error parsing sensor data: {e}")

    def send_motor_command(self, speed: int, angle: int) -> bool:
        """
        Send motor control command to Arduino

        Args:
            speed (int): Speed value (-255 to 255)
            angle (int): Angle value (-180 to 180)

        Returns:
            bool: True if command sent successfully, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            # Clamp values to valid ranges
            speed = max(-255, min(255, speed))
            angle = max(-180, min(180, angle))

            # Create motor command packet
            # Format: Header (1 byte) + Speed (2 bytes) + Angle (2 bytes) = 5 bytes total
            command_packet = struct.pack('<Bhh', self.MOTOR_HEADER_BYTE, speed, angle)

            # Send command
            bytes_written = self.serial_connection.write(command_packet)
            self.serial_connection.flush()  # Ensure data is sent immediately

            return bytes_written == len(command_packet)

        except (serial.SerialException, OSError, struct.error) as e:
            print(f"Error sending motor command: {e}")
            return False

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

    def close_connection(self) -> None:
        """Close serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.connected = False

    def __del__(self):
        """Destructor - ensure serial connection is closed"""
        self.close_connection()
