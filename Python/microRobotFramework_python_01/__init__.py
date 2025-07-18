"""
microRobotFramework Python Package
Python version of the microRobotFramework for 2-wheel robot control

This package provides:
- MRF class for robot control and sensor data reception
- Serial communication with microcontroller
- IMU and encoder data processing
"""

from .microRobotFramework import MRF

__version__ = "1.0.0"
__author__ = "JD-edu"
__email__ = ""
__description__ = "Python version of microRobotFramework for 2-wheel robot control"

# Package metadata
__all__ = [
    'MRF',
]

# Version info
VERSION = (1, 0, 0)
VERSION_STRING = '.'.join(map(str, VERSION))
