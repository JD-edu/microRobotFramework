# microRobotFramework Python Version 2.0

Python version of the microRobotFramework for 2-wheel robot control with **Motor Control Support**, converted from the original C++ implementation.

## 📋 Overview

This is **Version 2.0** of the Python port of the microRobotFramework C++ library from the [JD-edu/microRobotFramework](https://github.com/JD-edu/microRobotFramework) repository. 

### 🆕 What's New in Version 2.0

| Feature | Version 1.0 | Version 2.0 |
|---------|-------------|-------------|
| **IMU Data Reception** | ✅ Yes | ✅ Yes |
| **Encoder Data Reception** | ✅ Yes | ✅ Yes |
| **Motor Control Commands** | ❌ No | ✅ **NEW!** |
| **Serial Communication** | 📖 Read-Only | 📖📝 **Read & Write** |
| **Bidirectional Communication** | ❌ No | ✅ **NEW!** |

### 🎯 Key Features

- **📡 Sensor Data Reception**: Read IMU (accelerometer, gyroscope) and encoder data
- **🎮 Motor Control**: Send speed and angle commands to control 2-wheel robot
- **🔄 Bidirectional Communication**: Both receive sensor data and send motor commands
- **⚡ Real-time Processing**: Continuous sensor monitoring with motor control
- **🛡️ Buffer Protection**: Prevents Arduino serial buffer overflow
- **🖥️ Cross-platform**: Linux, Windows, macOS support

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Serial port access permissions
- Connected microRobot hardware with motor control support
- Arduino firmware that supports both sensor data transmission and motor command reception

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the basic example:
```bash
python3 mrf_example_02.py
```

3. Run the advanced motor control example:
```bash
python3 mrf_example_02.py --advanced
```

### Serial Port Configuration

Before running, make sure to update the serial port in the code:

- **Linux/macOS**: `/dev/ttyACM0`, `/dev/ttyUSB0`
- **Windows**: `COM3`, `COM4`, etc.

## 📁 File Structure

```
microRobotFramework_v2_python/
├── microRobotFramework_02.py    # Main MRF class with motor control
├── mrf_example_02.py            # Example usage with motor commands
├── requirements.txt             # Python dependencies
├── setup.py                     # Package installation script
├── __init__.py                  # Package initialization
└── README.md                    # This file
```

## 🔧 Usage

### Basic Usage with Motor Control

```python
from microRobotFramework_02 import MRF
import time

# Initialize MRF with serial port and baud rate
mrf = MRF("/dev/ttyACM0", 115200)

# Check connection
if not mrf.is_connected():
    print("Serial port is not connected")
    exit(1)

count = 0

# Main loop
while True:
    # Receive sensor data
    if mrf.receive_sensor_data():
        # Get accelerometer data
        accel_x = mrf.get_accel_x()
        accel_y = mrf.get_accel_y()
        accel_z = mrf.get_accel_z()

        print(f"Accel: X={accel_x}, Y={accel_y}, Z={accel_z}")

    # Send motor command every 100 sensor readings
    if count > 100:
        # Send motor command: speed=90, angle=100
        success = mrf.send_motor_command(90, 100)
        if success:
            print("Motor command sent successfully")
        count = 0
    else:
        count += 1

    time.sleep(0.001)  # 1ms delay
```

### Advanced Motor Control Patterns

```python
from microRobotFramework_02 import MRF
import time

mrf = MRF("/dev/ttyACM0", 115200)

# Different movement patterns
movements = [
    (100, 0),    # Forward
    (80, 45),    # Turn right
    (-80, 0),    # Backward
    (80, -45),   # Turn left
    (0, 0)       # Stop
]

for speed, angle in movements:
    mrf.send_motor_command(speed, angle)
    time.sleep(2)  # Execute each movement for 2 seconds
```

## 🎮 Motor Control API

### New Methods in Version 2.0

#### `send_motor_command(speed: int, angle: int) -> bool`

Send motor control command to Arduino.

**Parameters:**
- `speed` (int): Speed value (-255 to 255)
  - Positive values: Forward movement
  - Negative values: Backward movement
  - 0: Stop
- `angle` (int): Steering angle (-180 to 180)
  - Positive values: Turn right
  - Negative values: Turn left
  - 0: Straight

**Returns:**
- `bool`: True if command sent successfully, False otherwise

**Example:**
```python
# Move forward at speed 100
mrf.send_motor_command(100, 0)

# Turn right while moving forward
mrf.send_motor_command(80, 45)

# Move backward
mrf.send_motor_command(-100, 0)

# Stop the robot
mrf.send_motor_command(0, 0)
```

## 📊 Communication Protocol

### Sensor Data Reception (Unchanged from v1.0)
- **Packet Size**: 21 bytes
- **Header**: 0xF5
- **Data**: 20 bytes (6×int16 IMU + 4×uint16 Encoders)

### Motor Command Transmission (New in v2.0)
- **Packet Size**: 5 bytes
- **Header**: 0xFA
- **Data**: 4 bytes (2×int16: speed, angle)
- **Format**: `[0xFA][speed_low][speed_high][angle_low][angle_high]`

## ⚠️ Important Notes

### Serial Buffer Management

The example includes a "cooling down" mechanism to prevent Arduino serial buffer overflow:

```python
# Send motor commands every 100 sensor readings
if count > 100:
    mrf.send_motor_command(speed, angle)
    count = 0
```

**Why this is important:**
- Sending motor commands too frequently can freeze the Arduino serial buffer
- The current implementation is for study and testing purposes
- For production use, consider using separate threads for sensor reception and motor control

### Threading Recommendation

For advanced applications, consider using threading:

```python
import threading
import time
from microRobotFramework_02 import MRF

def sensor_thread(mrf):
    while True:
        if mrf.receive_sensor_data():
            # Process sensor data
            pass
        time.sleep(0.001)

def motor_thread(mrf):
    while True:
        # Send motor commands based on logic
        mrf.send_motor_command(speed, angle)
        time.sleep(0.1)  # 100ms interval

mrf = MRF("/dev/ttyACM0", 115200)

# Start threads
t1 = threading.Thread(target=sensor_thread, args=(mrf,))
t2 = threading.Thread(target=motor_thread, args=(mrf,))

t1.start()
t2.start()
```

## 🛠️ Troubleshooting

### Common Issues

1. **Motor Commands Not Working**
   - Ensure Arduino firmware supports motor control commands
   - Check if motor control header byte (0xFA) is correctly implemented
   - Verify motor hardware connections

2. **Serial Buffer Freeze**
   - Reduce motor command frequency
   - Implement proper timing between commands
   - Consider using separate threads

3. **Permission Denied**
   ```bash
   sudo chmod 666 /dev/ttyACM0
   # or add user to dialout group
   sudo usermod -a -G dialout $USER
   ```

## 🔄 Migration from Version 1.0

### Code Changes Required

1. **Import Statement**:
   ```python
   # Old (v1.0)
   from microRobotFramework import MRF

   # New (v2.0)
   from microRobotFramework_02 import MRF
   ```

2. **New Motor Control**:
   ```python
   # Add motor control to your existing code
   mrf.send_motor_command(speed, angle)
   ```

3. **Method Names** (Unchanged):
   - All sensor data methods remain the same
   - `receive_sensor_data()`, `get_accel_x()`, etc.

## 📈 Performance Considerations

- **Sensor Reading**: ~1ms interval recommended
- **Motor Commands**: ~100ms interval recommended (to prevent buffer overflow)
- **Memory Usage**: Minimal overhead for motor control functionality
- **CPU Usage**: Low impact, suitable for Raspberry Pi

## 🤝 Contributing

This is a direct port of the original C++ code with motor control enhancements. For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch
3. Test motor control functionality thoroughly
4. Submit a pull request

## 📄 License

This project maintains the same license as the original C++ version.

## 🔗 Related Links

- [Original C++ Repository](https://github.com/JD-edu/microRobotFramework)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [Version 1.0 Documentation](../microRobotFramework_01/)

## 📝 Version History

- **v2.0**: Added motor control functionality, bidirectional communication
- **v1.0**: Basic sensor data reception, read-only communication

---

**🎉 Ready to control your 2-wheel robot with Python!** 🤖
