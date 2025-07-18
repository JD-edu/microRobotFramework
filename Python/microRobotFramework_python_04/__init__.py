"""
microRobotFramework_04 Python Package
Python version of the microRobotFramework_04 for 2-wheel robot control with odometry

This package provides:
- MRF class for enhanced robot control with speed and angle-based motor commands
- MRF_Odometry class for real-time position and orientation tracking
- Serial communication with microcontroller
- IMU and encoder data processing
- Path recording and navigation statistics
- Interactive robot control examples

Version 04 Features:
- Enhanced motor control with differential drive kinematics
- Real-time odometry calculations
- Position and velocity tracking
- Path history recording
- Data logging and export capabilities
"""

from .microRobotFramework_04 import MRF
from .MRF_odometry import MRF_Odometry, Position, Velocity

__version__ = "1.0.0"
__author__ = "JD-edu"
__email__ = ""
__description__ = "Python version of microRobotFramework_04 for 2-wheel robot control with odometry"

# Package metadata
__all__ = [
    'MRF',
    'MRF_Odometry',
    'Position',
    'Velocity',
]

# Version info
VERSION = (1, 0, 0)
VERSION_STRING = '.'.join(map(str, VERSION))

# Feature flags
FEATURES = {
    'odometry': True,
    'enhanced_motor_control': True,
    'path_recording': True,
    'data_logging': True,
    'interactive_control': True,
}

def get_version():
    """Get package version string"""
    return VERSION_STRING

def get_features():
    """Get available features"""
    return FEATURES.copy()

def print_info():
    """Print package information"""
    print(f"microRobotFramework_04 v{VERSION_STRING}")
    print(f"Author: {__author__}")
    print(f"Description: {__description__}")
    print("Available features:")
    for feature, enabled in FEATURES.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature}")
