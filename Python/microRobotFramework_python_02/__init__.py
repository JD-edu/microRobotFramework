"""
microRobotFramework Python Package v2.0
Python version of the microRobotFramework for 2-wheel robot control with motor control support

This package provides:
- MRF class for robot control, sensor data reception, and motor control
- Bidirectional serial communication with microcontroller
- IMU and encoder data processing
- Motor speed and angle control commands
- Real-time sensor monitoring with motor control

Version 2.0 Features:
- ✅ Sensor data reception (IMU + Encoders)
- ✅ Motor control commands (Speed + Angle)
- ✅ Bidirectional serial communication
- ✅ Buffer overflow protection
- ✅ Cross-platform support
"""

from .microRobotFramework_02 import MRF

__version__ = "2.0.0"
__author__ = "JD-edu"
__email__ = ""
__description__ = "Python version of microRobotFramework v2.0 for 2-wheel robot control with motor control support"

# Package metadata
__all__ = [
    'MRF',
]

# Version info
VERSION = (2, 0, 0)
VERSION_STRING = '.'.join(map(str, VERSION))

# Feature flags
FEATURES = {
    'sensor_data_reception': True,
    'motor_control': True,
    'bidirectional_communication': True,
    'imu_support': True,
    'encoder_support': True,
    'cross_platform': True,
}

# Protocol constants
PROTOCOL = {
    'sensor_header_byte': 0xF5,
    'motor_header_byte': 0xFA,
    'sensor_packet_size': 21,  # 1 header + 20 data bytes
    'motor_packet_size': 5,    # 1 header + 4 data bytes
    'default_baud_rate': 115200,
}

def get_version():
    """Get package version string"""
    return __version__

def get_features():
    """Get available features"""
    return FEATURES.copy()

def get_protocol_info():
    """Get communication protocol information"""
    return PROTOCOL.copy()

# Compatibility check
def check_compatibility():
    """Check if the current environment supports all features"""
    import sys

    compatibility = {
        'python_version': sys.version_info >= (3, 7),
        'serial_support': True,
        'threading_support': True,
    }

    try:
        import serial
        compatibility['pyserial_available'] = True
    except ImportError:
        compatibility['pyserial_available'] = False

    return compatibility

# Quick start helper
def quick_start_info():
    """Display quick start information"""
    info = f"""
microRobotFramework v{__version__} - Quick Start
{'='*50}

1. Install dependencies:
   pip install -r requirements.txt

2. Basic usage:
   from microRobotFramework_02 import MRF

   mrf = MRF("/dev/ttyACM0", 115200)

   # Read sensor data
   if mrf.receive_sensor_data():
       print(f"Accel X: {{mrf.get_accel_x()}}")

   # Send motor command
   mrf.send_motor_command(100, 0)  # speed=100, angle=0

3. Run examples:
   python3 mrf_example_02.py
   python3 mrf_example_02.py --advanced

Features: {', '.join([k for k, v in FEATURES.items() if v])}
"""
    return info

if __name__ == "__main__":
    print(quick_start_info())
