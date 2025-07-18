"""
microRobotFramework_03.py
Python version of the microRobotFramework C++ class (Version 03)
Converted from microRobotFramework.hpp and microRobotFramework.cpp

Version 03 Features:
- Multi-threading support for concurrent sensor reading and motor control
- Speed and angle based motor control system
- Enhanced serial communication with mutex protection
- Real-time sensor data processing
"""

import serial
import struct
import time
import threading
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MRF:
    """
    MicroRobotFramework class Version 03 for 2-wheel robot control
    Features multi-threading support and enhanced motor control
    """

    # Constants
    HEADER_BYTE = 0xF5  # Header byte for sensor data reception
    MOTOR_HEADER = 0xAA  # Header byte for motor commands

    def __init__(self, port: str, baud_rate: int):
        """
        Constructor

        Args:
            port (str): Serial port path (e.g., '/dev/ttyUSB0', 'COM3')
            baud_rate (int): Baud rate for serial communication (e.g., 115200)
        """
        self.serial_port = port
        self.baud_rate = baud_rate
        self.connected = False
        self.serial_connection: Optional[serial.Serial] = None

        # Thread synchronization
        self.serial_mutex = threading.Lock()
        self.running = threading.Event()
        self.running.set()  # Initially running

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
            logger.info(f"Serial connection opened: {self.serial_port}")
            return True
        except (serial.SerialException, OSError) as e:
            logger.error(f"Error opening serial port {self.serial_port}: {e}")
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
        Receive sensor data from serial port (23 bytes total)
        Data format: [Header][Length][IMU Data (12 bytes)][Encoder Data (8 bytes)][Checksum]

        Returns:
            bool: True if data received successfully, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            with self.serial_mutex:  # Thread-safe serial access
                # Read 23 bytes as per C++ implementation
                data_buffer = self.serial_connection.read(23)
                if len(data_buffer) != 23:
                    return False

                # Parse the data (skip header and length bytes)
                self._parse_sensor_data(data_buffer[2:])  # Skip first 2 bytes
                return True

        except (serial.SerialException, OSError) as e:
            logger.error(f"Error reading sensor data: {e}")
            return False

    def _parse_sensor_data(self, data_buffer: bytes) -> None:
        """
        Parse sensor data from buffer (21 bytes of actual data)
        Data format: 6 int16 values (IMU) + 4 uint16 values (Encoders) + checksum

        Args:
            data_buffer (bytes): 21-byte data buffer
        """
        try:
            # Parse IMU data (12 bytes) - big-endian format as per C++ code
            self.accel_x = struct.unpack('>h', data_buffer[0:2])[0]
            self.accel_y = struct.unpack('>h', data_buffer[2:4])[0]
            self.accel_z = struct.unpack('>h', data_buffer[4:6])[0]
            self.gyro_x = struct.unpack('>h', data_buffer[6:8])[0]
            self.gyro_y = struct.unpack('>h', data_buffer[8:10])[0]
            self.gyro_z = struct.unpack('>h', data_buffer[10:12])[0]

            # Parse Encoder data (8 bytes) - big-endian format
            self.encoder1 = struct.unpack('>H', data_buffer[12:14])[0]
            self.encoder2 = struct.unpack('>H', data_buffer[14:16])[0]
            self.encoder3 = struct.unpack('>H', data_buffer[16:18])[0]
            self.encoder4 = struct.unpack('>H', data_buffer[18:20])[0]

        except struct.error as e:
            logger.error(f"Error parsing sensor data: {e}")

    def send_motor_command(self, speed: int, angle: int) -> bool:
        """
        Send motor control command with speed and angle
        Packet structure: [Header][Length][Speed][Angle][Checksum]

        Args:
            speed (int): Motor speed (0-255)
            angle (int): Steering angle (-127 to 127)

        Returns:
            bool: True if command sent successfully, False otherwise
        """
        if not self.is_connected():
            logger.error("Serial port not connected!")
            return False

        try:
            with self.serial_mutex:  # Thread-safe serial access
                # Validate input ranges
                speed = max(0, min(255, speed))  # Clamp to 0-255
                angle = max(-127, min(127, angle))  # Clamp to -127 to 127

                # Create packet as per C++ implementation
                packet = bytearray(5)
                packet[0] = self.MOTOR_HEADER  # Header byte (0xAA)
                packet[1] = 3  # Length byte (speed + angle + checksum)
                packet[2] = speed & 0xFF  # Speed byte
                packet[3] = angle & 0xFF  # Angle byte (handle negative values)
                packet[4] = packet[0] ^ packet[1] ^ packet[2] ^ packet[3]  # XOR checksum

                # Send packet
                bytes_written = self.serial_connection.write(packet)
                if bytes_written != len(packet):
                    logger.error("Failed to send complete motor command!")
                    return False

                return True

        except (serial.SerialException, OSError) as e:
            logger.error(f"Error sending motor command: {e}")
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

    def stop_threads(self) -> None:
        """Stop all running threads"""
        self.running.clear()

    def close_connection(self) -> None:
        """Close serial connection and stop threads"""
        self.stop_threads()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info("Serial connection closed")
        self.connected = False

    def __del__(self):
        """Destructor - ensure serial connection is closed"""
        self.close_connection()


# Thread-safe functions for multi-threading support
class MRFThreadManager:
    """
    Thread manager for MRF operations
    Handles concurrent sensor reading and motor control
    """

    def __init__(self, mrf_instance: MRF):
        self.mrf = mrf_instance
        self.sensor_thread = None
        self.motor_thread = None

    def start_sensor_thread(self, read_interval: float = 0.05):
        """
        Start sensor data reading thread

        Args:
            read_interval (float): Reading interval in seconds (default: 50ms)
        """
        def sensor_reader():
            while self.mrf.running.is_set():
                if self.mrf.receive_sensor_data():
                    logger.debug(f"Sensor data: AccelX={self.mrf.get_accel_x()}, "
                               f"AccelY={self.mrf.get_accel_y()}, "
                               f"AccelZ={self.mrf.get_accel_z()}")
                time.sleep(read_interval)

        self.sensor_thread = threading.Thread(target=sensor_reader, daemon=True)
        self.sensor_thread.start()
        logger.info("Sensor reading thread started")

    def start_motor_thread(self, speed: int = 90, angle: int = 100, 
                          command_interval: float = 0.1):
        """
        Start motor command sending thread

        Args:
            speed (int): Motor speed (0-255)
            angle (int): Steering angle (-127 to 127)
            command_interval (float): Command sending interval in seconds (default: 100ms)
        """
        def motor_commander():
            while self.mrf.running.is_set():
                self.mrf.send_motor_command(speed, angle)
                time.sleep(command_interval)

        self.motor_thread = threading.Thread(target=motor_commander, daemon=True)
        self.motor_thread.start()
        logger.info(f"Motor command thread started (Speed={speed}, Angle={angle})")

    def stop_all_threads(self):
        """Stop all threads"""
        self.mrf.stop_threads()

        if self.sensor_thread and self.sensor_thread.is_alive():
            self.sensor_thread.join(timeout=1.0)

        if self.motor_thread and self.motor_thread.is_alive():
            self.motor_thread.join(timeout=1.0)

        logger.info("All threads stopped")
