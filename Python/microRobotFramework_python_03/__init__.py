"""
microRobotFramework_03 Python Package
Python version of the microRobotFramework Version 03 with multi-threading support

This package provides:
- MRF class for robot control with multi-threading capabilities
- MRFThreadManager for concurrent sensor reading and motor control
- Thread-safe serial communication with microcontroller
- Real-time IMU and encoder data processing
- Speed and angle based motor control system

Version 03 Features:
- Multi-threading support for concurrent operations
- Thread-safe serial communication using mutex
- Enhanced motor control with speed and angle parameters
- Real-time sensor data processing
- Advanced control patterns and sequences
"""

from .microRobotFramework_03 import MRF, MRFThreadManager

__version__ = "3.0.0"
__author__ = "JD-edu"
__email__ = ""
__description__ = "Python version of microRobotFramework Version 03 with multi-threading support"

# Package metadata
__all__ = [
    'MRF',
    'MRFThreadManager',
]

# Version info
VERSION = (3, 0, 0)
VERSION_STRING = '.'.join(map(str, VERSION))

# Feature flags
FEATURES = {
    'multi_threading': True,
    'motor_control': True,
    'sensor_reading': True,
    'thread_safe_communication': True,
    'speed_angle_control': True,
    'real_time_processing': True,
}

def get_version():
    """Get package version string"""
    return VERSION_STRING

def get_features():
    """Get available features"""
    return FEATURES.copy()

def print_info():
    """Print package information"""
    print(f"microRobotFramework Version {VERSION_STRING}")
    print("Features:")
    for feature, enabled in FEATURES.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature.replace('_', ' ').title()}")
