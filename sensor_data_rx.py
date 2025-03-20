import serial
import struct
ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, timeout=1)

while True:
    data_raw = ser.read(29)

    if data_raw[0] != 0xf5:
        print("wrong header")
        continue

    data = data_raw[2:28] 

    if len(data) == 26:
        ax, ay, az, gx, gy, gx, pitch, roll, yaw, e1, e2, e3, e4= struct.unpack('<hhhhhhhhhhhhh', data)
        print(f"pitch: {pitch}, roll: {roll}, yaw: {yaw}, e1: {e1}, e2: {e2}, e3: {e3}, e4: {e4}")