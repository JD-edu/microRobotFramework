import serial
import struct

ser = serial.Serial('/dev/ttyUSB0', 115200)

while True:
    data = ser.read(12)  # Read 12 bytes
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = struct.unpack('<hhhhhh', data)

    print(f"Acc: X={acc_x}, Y={acc_y}, Z={acc_z} | Gyro: X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
