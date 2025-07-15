import serial
import struct
import time

# Set the serial port (Change to your actual port, e.g., COM3 on Windows or /dev/ttyUSB0 on Linux/macOS)
SERIAL_PORT = "/dev/ttyACM0"  # Update this to match your setup
BAUD_RATE = 115200
HEADER_BYTE = 0xF5 # 아두이노에서 보낼 헤더 바이트 (예시)

def read_mpu_data():
    ser = None # ser 변수를 미리 선언하여 finally 블록에서 접근 가능하도록 함
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        while True:
            # 헤더 바이트(0xF5)를 찾을 때까지 바이트를 읽음
            byte = ser.read(1)
            if not byte: # 타임아웃으로 아무 바이트도 읽지 못했을 경우
                continue

            if ord(byte) == HEADER_BYTE:
                # 헤더 다음의 22바이트를 읽으려고 시도 (총 23바이트 패킷 중 헤더 제외)
                remaining_data = ser.read(22)
                
                # 읽어온 데이터의 길이가 정확히 22바이트인지 확인
                if len(remaining_data) == 22:
                    data = remaining_data[0:20] # 헤더 다음 2바이트를 건너뛰고 20바이트 추출
                    try:
                        # ">hhhhhhhhhh"는 10개의 short (2바이트) 값을 나타내므로 총 20바이트
                        accelX, accelY, accelZ, gX, gY, gZ, e1, e2, e3, e4 = struct.unpack(">hhhhhhhhhh", data)
                        print(f"Accel: X={accelX}, Y={accelY}, Z={accelZ}, Gyro: X={gX}, Y={gY}, Z={gZ}")
                        # 필요한 경우 나머지 e1, e2, e3, e4 값도 출력 가능
                    except struct.error as se:
                        print(f"Struct unpack error: {se}. Data length: {len(data)}. Data: {data.hex()}")
                        # unpack 오류 발생 시, 어떤 데이터가 문제였는지 확인하기 위함
                else:
                    print(f"Incomplete packet received. Expected 22 bytes after header, got {len(remaining_data)} bytes.")
                    # 불완전한 패킷 수신 시 경고
            # else: # 헤더 바이트가 아닐 경우 다음 바이트를 계속 확인
            #     print(f"Skipping byte: {ord(byte)}") # 디버깅용: 스킵하는 바이트 확인

    except serial.SerialException as e:
        print(f"Error: {e}. Please check if the port is correct and not in use.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally: # 프로그램 종료 시 시리얼 포트를 항상 닫도록 함
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    read_mpu_data()