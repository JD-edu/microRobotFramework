"""
microRobotFramework.py
Python version of the microRobotFramework C++ class for 2-wheel robot control
Converted from microRobotFramework.hpp and microRobotFramework.cpp
"""

import serial
import struct
import time
import errno
from typing import Optional, Tuple


class MRF:
    """
    MicroRobotFramework class for 2-wheel robot control
    Handles serial communication, sensor data reception (IMU + Encoder)
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
        Reads 21 bytes total: 1 header byte + 20 data bytes

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

            # 2. Read remaining 22 bytes of data, extract 20 bytes excluding length
            data = self.serial_connection.read(20)
            #data = remaining_data[0:20]
        
            # 3. Parse the data
            self._parse_sensor_data(data)
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
            self.accel_x, self.accel_y, self.accel_z, self.gyro_x, self.gyro_y, self.gyro_z, self.encoder1, self.encoder2, self.encoder3, self.encoder4 = struct.unpack(">hhhhhhhhhh", data_buffer)

        except struct.error as e:
            print(f"Error parsing sensor data: {e}")

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
