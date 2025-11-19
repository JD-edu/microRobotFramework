### **📌 Packet Structure for Serial Communication**
The **Arduino code** sends sensor data over **serial communication** in a structured **23-byte packet**. This packet contains IMU (MPU6050) data, encoder values, and a checksum. Below is a breakdown of the **packet structure**:

---

## **📜 Packet Format**
| **Byte Index** | **Field Name** | **Description** | **Size (Bytes)** |
|--------------|--------------|------------------------------------------------------|-------------|
| `0` | **Header** | Start-of-frame marker (fixed value `0xF5`) | 1 |
| `1` | **Length** | Number of bytes in the packet (fixed `21`) | 1 |
| `2-3` | **AccelX** | 16-bit signed integer (`int16_t`) | 2 |
| `4-5` | **AccelY** | 16-bit signed integer (`int16_t`) | 2 |
| `6-7` | **AccelZ** | 16-bit signed integer (`int16_t`) | 2 |
| `8-9` | **GyroX** | 16-bit signed integer (`int16_t`) | 2 |
| `10-11` | **GyroY** | 16-bit signed integer (`int16_t`) | 2 |
| `12-13` | **GyroZ** | 16-bit signed integer (`int16_t`) | 2 |
| `14-15` | **Encoder1** | 16-bit unsigned integer (`uint16_t`) | 2 |
| `16-17` | **Encoder2** | 16-bit unsigned integer (`uint16_t`) | 2 |
| `18-19` | **Encoder3** | 16-bit unsigned integer (`uint16_t`) | 2 |
| `20-21` | **Encoder4** | 16-bit unsigned integer (`uint16_t`) | 2 |
| `22` | **Checksum** | Placeholder (`0`, not implemented yet) | 1 |

- **Total Packet Size:** `23 bytes`

---

## **📌 Explanation of Each Field**
### **1️⃣ Header (`0xF5` - 1 Byte)**
- **Purpose:** Identifies the start of a valid packet.
- **Why?** This ensures that the receiver can synchronize correctly.

### **2️⃣ Length (`0x15` or `21` - 1 Byte)**
- **Purpose:** Indicates how many bytes follow this field.
- **Why?** Helps the receiver know when the packet ends.

### **3️⃣ Accelerometer Data (`AccelX`, `AccelY`, `AccelZ` - 6 Bytes)**
- **Format:** Each accelerometer axis (`X, Y, Z`) is a **16-bit signed integer (`int16_t`)**.
- **Scaling:** Multiplied by **1000** before sending to keep precision (`m/s²` × 1000).

### **4️⃣ Gyroscope Data (`GyroX`, `GyroY`, `GyroZ` - 6 Bytes)**
- **Format:** Each gyroscope axis (`X, Y, Z`) is a **16-bit signed integer (`int16_t`)**.
- **Scaling:** Multiplied by **1000** before sending to keep precision (`°/s` × 1000).

### **5️⃣ Encoder Data (`Encoder1`, `Encoder2`, `Encoder3`, `Encoder4` - 8 Bytes)**
- **Format:** Each encoder value is a **16-bit unsigned integer (`uint16_t`)**.
- **Purpose:** Simulated encoder counts for wheels.

### **6️⃣ Checksum (Placeholder - 1 Byte)**
- **Currently set to `0`** (not implemented).
- **Purpose:** Intended to verify packet integrity.
- **Future Implementation:** Could be **XOR checksum** or **CRC-8**.

---

## **📌 Example Packet (Hex Representation)**
| **Byte** | **Value (Example)** | **Description** |
|---------|----------------|------------------|
| `0` | `F5` | Header |
| `1` | `15` | Length (21) |
| `2-3` | `03 E8` | AccelX = `1000` (1.0 m/s²) |
| `4-5` | `FF 9C` | AccelY = `-100` (-0.1 m/s²) |
| `6-7` | `00 64` | AccelZ = `100` (0.1 m/s²) |
| `8-9` | `00 32` | GyroX = `50` (0.05 °/s) |
| `10-11` | `FF CE` | GyroY = `-50` (-0.05 °/s) |
| `12-13` | `00 19` | GyroZ = `25` (0.025 °/s) |
| `14-15` | `00 01` | Encoder1 = `1` |
| `16-17` | `00 02` | Encoder2 = `2` |
| `18-19` | `00 03` | Encoder3 = `3` |
| `20-21` | `00 04` | Encoder4 = `4` |
| `22` | `00` | Checksum (placeholder) |

---

## **📌 How to Parse This Packet in Python**
A **Python script** can read and extract **sensor data** using the `struct` module.

```python
import serial
import struct

# Set up serial port (modify according to your system)
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

def read_mpu_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        while True:
            packet = ser.read(23)  # Read full packet
            
            if len(packet) == 23 and packet[0] == 0xF5:  # Check header
                data = packet[2:22]  # Extract sensor data
                accelX, accelY, accelZ, gX, gY, gZ, e1, e2, e3, e4 = struct.unpack(">hhhhhhhhhh", data)

                print(f"AccelX: {accelX}, AccelY: {accelY}, AccelZ: {accelZ}")
                print(f"GyroX: {gX}, GyroY: {gY}, GyroZ: {gZ}")
                print(f"Encoders: {e1}, {e2}, {e3}, {e4}")

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()

if __name__ == "__main__":
    read_mpu_data()
```

---

## **📌 Future Improvements**
### **1️⃣ Implement Checksum**
Currently, the **checksum** is not used. It can be added for **error detection**:
```cpp
data[22] = data[0] ^ data[1] ^ ... ^ data[21];  // XOR Checksum
```
On **Python**, verify:
```python
checksum = packet[0] ^ packet[1] ^ ... ^ packet[21]
if checksum == packet[22]:
    print("Valid packet")
else:
    print("Checksum mismatch")
```

### **2️⃣ Add CRC for Robust Error Checking**
Instead of XOR, **CRC-8 or CRC-16** can be implemented.

### **3️⃣ Implement Two-Way Communication**
- Raspberry Pi can **send commands** to control actuators (e.g., motor speed).
- Arduino will **execute commands** based on received instructions.

---

## **📌 Summary**
✅ **Packet Structure**: Organized **23-byte packet** for reliable serial communication.  
✅ **Data Fields**: **IMU (Accel & Gyro)**, **Encoder values**, **Header, Length, Checksum**.  
✅ **Python Parsing**: Extract sensor values efficiently using **struct.unpack()**.  
✅ **Next Steps**: **Implement checksum**, **CRC error detection**, and **bidirectional control**.  

---

### 🚀 **Now You're Ready for the Next Step!**
Would you like to implement **real-time graphing** of IMU data using **Matplotlib** in Step 2? 📊🔥
