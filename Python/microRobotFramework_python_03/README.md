# microRobotFramework Python Version 03

Python version of the microRobotFramework for 2-wheel robot control with **multi-threading support**, converted from the original C++ implementation.

## 📋 Overview

This is a Python port of the microRobotFramework C++ library Version 03 from the [JD-edu/microRobotFramework](https://github.com/JD-edu/microRobotFramework) repository. Version 03 introduces **multi-threading capabilities** for concurrent sensor data reading and motor control operations.

### 🆕 Version 03 Features

- **Multi-threading Support**: Concurrent sensor reading and motor control
- **Thread-safe Serial Communication**: Mutex-protected serial port access
- **Speed & Angle Motor Control**: Enhanced motor control system
- **Real-time Data Processing**: Continuous sensor monitoring with threading
- **Advanced Control Patterns**: Pre-defined motor movement sequences
- **Graceful Shutdown**: Proper thread cleanup and resource management

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Serial port access permissions
- Connected microRobot hardware

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the basic example:
```bash
python3 mrf_example_03.py
```

### Serial Port Configuration

Before running, make sure to update the serial port in the code:

- **Linux/macOS**: `/dev/ttyUSB0`, `/dev/ttyACM0`
- **Windows**: `COM3`, `COM4`, etc.

## 📁 File Structure

```
microRobotFramework_03_python/
├── microRobotFramework_03.py    # Main MRF class with multi-threading
├── mrf_example_03.py           # Multi-threading examples
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── setup.py                    # Package installation script
└── __init__.py                 # Package initialization
```

## 🔧 Usage

### Basic Multi-threading Usage

```python
from microRobotFramework_03 import MRF, MRFThreadManager
import time

# Initialize MRF
mrf = MRF("/dev/ttyUSB0", 115200)
thread_manager = MRFThreadManager(mrf)

# Check connection
if not mrf.is_connected():
    print("Serial port is not connected")
    exit(1)

# Start sensor reading thread (50ms interval)
thread_manager.start_sensor_thread(read_interval=0.05)

# Start motor command thread (speed=90, angle=100, 100ms interval)
thread_manager.start_motor_thread(speed=90, angle=100, command_interval=0.1)

# Main loop - display data
try:
    while True:
        accel_x = mrf.get_accel_x()
        accel_y = mrf.get_accel_y()
        accel_z = mrf.get_accel_z()

        print(f"Accel: X={accel_x}, Y={accel_y}, Z={accel_z}")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    thread_manager.stop_all_threads()
    mrf.close_connection()
```

### Advanced Motor Control

```python
from microRobotFramework_03 import MRF

mrf = MRF("/dev/ttyUSB0", 115200)

# Speed and angle based control
mrf.send_motor_command(speed=100, angle=0)    # Forward
mrf.send_motor_command(speed=80, angle=50)    # Turn right
mrf.send_motor_command(speed=80, angle=-50)   # Turn left
mrf.send_motor_command(speed=0, angle=0)      # Stop
```

## 🧵 Multi-threading Architecture

### Thread Types

1. **Sensor Reading Thread**
   - Continuously reads IMU and encoder data
   - Configurable reading interval (default: 50ms)
   - Thread-safe data storage

2. **Motor Command Thread**
   - Sends periodic motor control commands
   - Configurable command interval (default: 100ms)
   - Speed and angle based control

3. **Main Thread**
   - User interface and data display
   - Thread coordination and cleanup

### Thread Safety

- **Mutex Protection**: All serial communication is protected by threading locks
- **Atomic Operations**: Thread-safe data access for sensor values
- **Graceful Shutdown**: Proper thread cleanup on exit

## 📊 Available Methods

### Connection Methods
- `is_connected()` - Check if serial connection is active
- `close_connection()` - Close serial connection and stop threads

### Data Reception
- `receive_sensor_data()` - Read sensor data from serial port (thread-safe)

### Motor Control
- `send_motor_command(speed, angle)` - Send speed and angle based commands
  - `speed`: 0-255 (motor speed)
  - `angle`: -127 to 127 (steering angle)

### IMU Data Getters
- `get_accel_x()`, `get_accel_y()`, `get_accel_z()` - Accelerometer data
- `get_gyro_x()`, `get_gyro_y()`, `get_gyro_z()` - Gyroscope data

### Encoder Data Getters
- `get_encoder1()`, `get_encoder2()`, `get_encoder3()`, `get_encoder4()` - Encoder values

### Thread Management
- `MRFThreadManager` class for managing concurrent operations
- `start_sensor_thread(read_interval)` - Start sensor reading thread
- `start_motor_thread(speed, angle, command_interval)` - Start motor command thread
- `stop_all_threads()` - Stop all running threads

## 🔄 Version 03 Improvements

### Multi-threading Features

| Feature | Description |
|---------|-------------|
| **Concurrent Operations** | Sensor reading and motor control run simultaneously |
| **Thread-safe Communication** | Mutex-protected serial port access |
| **Configurable Intervals** | Adjustable timing for sensor reading and motor commands |
| **Resource Management** | Proper thread cleanup and resource deallocation |

### Enhanced Motor Control

| Parameter | Range | Description |
|-----------|-------|-------------|
| **Speed** | 0-255 | Motor speed control |
| **Angle** | -127 to 127 | Steering angle control |
| **Command Interval** | Configurable | Motor command sending frequency |

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   sudo chmod 666 /dev/ttyUSB0
   # or add user to dialout group
   sudo usermod -a -G dialout $USER
   ```

2. **Port Not Found**
   - Check if device is connected: `ls /dev/tty*`
   - Verify correct port name in code

3. **Thread Synchronization Issues**
   - Ensure proper thread cleanup with `stop_all_threads()`
   - Use Ctrl+C for graceful shutdown

4. **No Data Received**
   - Check baud rate (default: 115200)
   - Verify hardware is sending data with correct protocol

## 📊 Data Protocol

### Sensor Data (23 bytes)
- 2 bytes: Header and Length
- 12 bytes: IMU data (6 × int16: accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
- 8 bytes: Encoder data (4 × uint16: encoder1, encoder2, encoder3, encoder4)
- 1 byte: Checksum

### Motor Command (5 bytes)
- 1 byte: Header (0xAA)
- 1 byte: Length (3)
- 1 byte: Speed (0-255)
- 1 byte: Angle (-127 to 127)
- 1 byte: XOR Checksum

## 🎯 Example Applications

### 1. Basic Multi-threading
```bash
python3 mrf_example_03.py
# Select option 1 for basic example
```

### 2. Advanced Motor Patterns
```bash
python3 mrf_example_03.py
# Select option 2 for advanced patterns
```

## 🤝 Contributing

This is a direct port of the original C++ code with multi-threading enhancements. For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with multi-threading scenarios
5. Submit a pull request

## 📄 License

This project maintains the same license as the original C++ version.

## 🔗 Related Links

- [Original C++ Repository](https://github.com/JD-edu/microRobotFramework)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)

## 🏆 Version History

- **Version 01**: Basic sensor data reception
- **Version 02**: Added motor control capabilities
- **Version 03**: Multi-threading support and enhanced motor control ⭐
