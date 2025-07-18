# microRobotFramework Python Version

Python version of the microRobotFramework for 2-wheel robot control, converted from the original C++ implementation.

## 📋 Overview

This is a Python port of the microRobotFramework C++ library from the [JD-edu/microRobotFramework](https://github.com/JD-edu/microRobotFramework) repository. The framework provides basic functionality for controlling 2-wheel robots through serial communication, including:

- **Serial Communication**: Connect to robot via USB/Serial port
- **Sensor Data Reception**: Read IMU (accelerometer, gyroscope) and encoder data
- **Real-time Data Processing**: Continuous sensor data monitoring

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

2. Run the example:
```bash
python3 mrf_example_01.py
```

### Serial Port Configuration

Before running, make sure to update the serial port in the code:

- **Linux/macOS**: `/dev/ttyACM0`, `/dev/ttyUSB0`
- **Windows**: `COM3`, `COM4`, etc.

## 📁 File Structure

```
microRobotFramework_python/
├── microRobotFramework.py    # Main MRF class (converted from .hpp/.cpp)
├── mrf_example_01.py         # Example usage (converted from .cpp)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔧 Usage

### Basic Usage

```python
from microRobotFramework import MRF
import time

# Initialize MRF with serial port and baud rate
mrf = MRF("/dev/ttyACM0", 115200)

# Check connection
if not mrf.is_connected():
    print("Serial port is not connected")
    exit(1)

# Main loop
while True:
    if mrf.receive_sensor_data():
        # Get accelerometer data
        accel_x = mrf.get_accel_x()
        accel_y = mrf.get_accel_y()
        accel_z = mrf.get_accel_z()

        print(f"Accel: X={accel_x}, Y={accel_y}, Z={accel_z}")

    time.sleep(0.005)  # 5ms delay
```

### Available Methods

#### Connection Methods
- `is_connected()` - Check if serial connection is active
- `close_connection()` - Close serial connection

#### Data Reception
- `receive_sensor_data()` - Read sensor data from serial port

#### IMU Data Getters
- `get_accel_x()`, `get_accel_y()`, `get_accel_z()` - Accelerometer data
- `get_gyro_x()`, `get_gyro_y()`, `get_gyro_z()` - Gyroscope data

#### Encoder Data Getters
- `get_encoder1()`, `get_encoder2()`, `get_encoder3()`, `get_encoder4()` - Encoder values

## 🔄 Conversion Details

### C++ to Python Mapping

| C++ Feature | Python Equivalent |
|-------------|-------------------|
| `#include <serial.h>` | `import serial` |
| `int16_t`, `uint16_t` | `int` with struct packing |
| `std::string` | `str` |
| `bool` | `bool` |
| File descriptors | `serial.Serial` object |
| Manual memory management | Automatic garbage collection |

### Key Changes

1. **Memory Management**: Python handles memory automatically
2. **Error Handling**: Uses Python exceptions instead of return codes
3. **Type Safety**: Added type hints for better code documentation
4. **Serial Communication**: Uses `pyserial` library instead of low-level system calls
5. **Data Parsing**: Uses `struct.unpack()` for binary data parsing

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

## 📊 Data Protocol

The framework expects 21-byte packets:
- 1 byte: Header (0xF5)
- 20 bytes: Sensor data
  - 6 × int16: IMU data (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
  - 4 × uint16: Encoder data (encoder1, encoder2, encoder3, encoder4)

## 🤝 Contributing

This is a direct port of the original C++ code. For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project maintains the same license as the original C++ version.

## 🔗 Related Links

- [Original C++ Repository](https://github.com/JD-edu/microRobotFramework)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
