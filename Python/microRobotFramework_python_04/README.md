# microRobotFramework Python Version 04

Python version of the microRobotFramework for 2-wheel robot control with odometry support, converted from the original C++ implementation.

## 📋 Overview

This is a Python port of the microRobotFramework C++ library version 04 from the [JD-edu/microRobotFramework](https://github.com/JD-edu/microRobotFramework) repository. This version includes enhanced motor control and odometry capabilities for precise robot navigation.

### Key Features

- **Enhanced Motor Control**: Speed and angle-based differential drive control
- **Odometry System**: Real-time position and orientation tracking
- **Sensor Data Reception**: IMU (accelerometer, gyroscope) and encoder data
- **Path Recording**: Automatic path history and statistics
- **Real-time Monitoring**: Live sensor data display and logging
- **Interactive Control**: Menu-driven robot operation

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Serial port access permissions
- Connected microRobot hardware with odometry support

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the example:
```bash
python3 mrf_example_04.py
```

### Serial Port Configuration

Before running, make sure to update the serial port in the code:

- **Linux/macOS**: `/dev/ttyACM0`, `/dev/ttyUSB0`
- **Windows**: `COM3`, `COM4`, etc.

## 📁 File Structure

```
microRobotFramework_04_python/
├── microRobotFramework_04.py    # Main MRF class with enhanced motor control
├── MRF_odometry.py             # Odometry calculation class
├── mrf_example_04.py           # Interactive example application
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation script
├── __init__.py                 # Package initialization
└── README.md                   # This file
```

## 🔧 Usage

### Basic Usage

```python
from microRobotFramework_04 import MRF
from MRF_odometry import MRF_Odometry
import time

# Initialize robot and odometry
robot = MRF("/dev/ttyACM0", 115200)
odometry = MRF_Odometry(wheel_base=0.2, wheel_radius=0.05)

# Check connection
if not robot.is_connected():
    print("Serial port is not connected")
    exit(1)

# Main control loop
while True:
    # Receive sensor data
    if robot.receive_sensor_data():
        # Update odometry
        encoder_left = robot.get_encoder1()
        encoder_right = robot.get_encoder2()
        odometry.update_odometry(encoder_left, encoder_right)

        # Get current position
        position = odometry.get_position()
        print(f"Position: ({position.x:.3f}, {position.y:.3f}, {position.theta:.3f})")

        # Control robot
        robot.send_motor_command(speed=50, angle=10)  # Move forward with slight right turn

    time.sleep(0.01)
```

### Available Methods

#### MRF Class (Enhanced Motor Control)
- `send_motor_command(speed, angle)` - Enhanced motor control with speed and steering angle
- `move_forward(speed)`, `move_backward(speed)` - Basic movement commands
- `turn_left(speed, angle)`, `turn_right(speed, angle)` - Turning commands
- `stop_motors()` - Stop all motors
- `receive_sensor_data()` - Read sensor data from serial port
- `get_accel_x/y/z()`, `get_gyro_x/y/z()` - IMU data getters
- `get_encoder1/2/3/4()` - Encoder data getters

#### MRF_Odometry Class
- `update_odometry(encoder_left, encoder_right)` - Update position calculations
- `get_position()`, `get_velocity()` - Get current state
- `reset_odometry()` - Reset to origin
- `set_position(x, y, theta)` - Set position manually
- `calculate_distance_to_point(x, y)` - Distance to target
- `get_statistics()` - Get odometry statistics
- `export_path_to_dict()` - Export path history

## 🎮 Interactive Example Features

The `mrf_example_04.py` provides an interactive menu system:

1. **Real-time Monitoring**: Live sensor data and position display
2. **Basic Movement Demo**: Automated movement sequence
3. **Square Pattern Demo**: Autonomous square path navigation
4. **Data Logging**: Save sensor and odometry data to JSON
5. **Statistics Display**: View odometry statistics and path info

## 🔄 Version 04 Enhancements

### Enhanced Motor Control
- **Speed + Angle Control**: More intuitive robot control interface
- **Differential Drive**: Automatic left/right wheel speed calculation
- **Smooth Steering**: Gradual turning based on angle parameter

### Odometry System
- **Position Tracking**: Real-time X, Y, θ position calculation
- **Velocity Estimation**: Linear and angular velocity computation
- **Path Recording**: Automatic path history with configurable buffer
- **Statistics**: Distance traveled, rotation, path length metrics

### Data Logging
- **JSON Export**: Structured data export for analysis
- **Real-time Logging**: Continuous data recording during operation
- **Path History**: Complete trajectory recording with timestamps

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   sudo chmod 666 /dev/ttyACM0
   # or add user to dialout group
   sudo usermod -a -G dialout $USER
   ```

2. **Port Not Found**
   - Check if device is connected: `ls /dev/tty*`
   - Verify correct port name in code

3. **No Data Received**
   - Check baud rate (default: 115200)
   - Verify hardware is sending data with correct protocol

4. **Odometry Drift**
   - Calibrate wheel parameters (wheel_base, wheel_radius)
   - Check encoder resolution settings
   - Verify encoder connections

## 📊 Data Protocol

The framework expects sensor data packets:
- **23 bytes total**: Header + sensor data
- **IMU data**: 6 × int16 (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
- **Encoder data**: 4 × uint16 (encoder1, encoder2, encoder3, encoder4)

Motor commands:
- **5 bytes**: Header (0xFA) + left_speed (int16) + right_speed (int16)

## 🤝 Contributing

This is a direct port of the original C++ code. For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with hardware
5. Submit a pull request

## 📄 License

This project maintains the same license as the original C++ version.

## 🔗 Related Links

- [Original C++ Repository](https://github.com/JD-edu/microRobotFramework)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [Differential Drive Kinematics](https://en.wikipedia.org/wiki/Differential_wheeled_robot)

## 📈 Performance Notes

- **Update Rate**: Recommended 10-100Hz for sensor data
- **Odometry Accuracy**: Depends on wheel parameter calibration
- **Memory Usage**: Path history limited to 1000 points by default
- **CPU Usage**: Minimal overhead for real-time operation

## 🎯 Future Enhancements

- **Kalman Filter**: Sensor fusion for improved odometry
- **Path Planning**: Automated navigation to waypoints
- **PID Control**: Closed-loop position control
- **Visualization**: Real-time path plotting
- **ROS Integration**: Robot Operating System compatibility
