import serial
import struct

# Set the serial port (Change to your actual port, e.g., COM3 on Windows or /dev/ttyUSB0 on Linux/macOS)
SERIAL_PORT = "/dev/ttyUSB0"  # Update this to match your setup
BAUD_RATE = 115200

def read_mpu_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        while True:
            # Look for the header byte 0xF5
            packet = ser.read(23)
            data = packet[2:22]
            accelX, accelY, accelZ, gX, gY, gZ, e1, e2, e3, e4 = struct.unpack(">hhhhhhhhhh", data)
            print(accelX, accelY, accelZ)
           
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()

if __name__ == "__main__":
    read_mpu_data()
