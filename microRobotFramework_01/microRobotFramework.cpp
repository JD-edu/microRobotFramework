#include "microRobotFramework.hpp"
#include <fcntl.h>    // For O_RDWR, O_NOCTTY, etc.
#include <unistd.h>   // For close()
#include <termios.h>  // For configuring serial port settings
#include <cstring>    // For memset()
#include <iostream>

// Constructor
MRF::MRF(const std::string& port, int baud)
    : serial_port(port), baud_rate(baud_rate), connected(false),
      accel_x(0), accel_y(0), accel_z(0),
      gyro_x(0), gyro_y(0), gyro_z(0),
      pitch(0), roll(0), yaw(0),
      encoder1(0), encoder2(0), encoder3(0), encoder4(0) {
    serial_port = port;
    baud_rate = baud;

    connected = openSerial();
}


// MRF 클래스의 멤버 변수와 함수 정의 (microRobotFramework.h 또는 microRobotFramework.cpp 상단에 정의되어 있다고 가정)
// 예를 들어:
// class MRF {
// public:
//     int serial_fd;
//     int16_t accel_x, accel_y, accel_z;
//     int16_t gyro_x, gyro_y, gyro_z;
//     uint16_t encoder1, encoder2, encoder3, encoder4;
//     // ... other members
// private:
//     static const uint8_t HEADER_BYTE = 0xF5; // Python 코드의 HEADER_BYTE와 일치
// };

// 현재 MRF 클래스 내부라고 가정하고 함수를 작성합니다.
bool MRF::receiveSensorData() {
    uint8_t header_buffer[1]; // 헤더 바이트를 읽기 위한 버퍼
    uint8_t data_buffer[20];  // 헤더를 제외한 20바이트 데이터를 위한 버퍼
    int bytes_read;

    // 1. 헤더 바이트(0xF5)를 찾을 때까지 1바이트씩 읽는다.
    while (true) {
        bytes_read = read(serial_fd, header_buffer, 1);
        if (bytes_read == 0) { // 타임아웃 (non-blocking 모드일 경우)
            // 데이터가 없음. 다시 시도
            //std::cout << "No data, retrying header read..." << std::endl; // Debugging
            return false; // 데이터가 없으므로 다음 루프에서 다시 시도
        }
        if (bytes_read == -1) { // read 에러 발생
            std::cerr << "Error reading serial port for header: " << strerror(errno) << std::endl; // Debugging
            return false; // 에러 발생
        }

        if (header_buffer[0] == HEADER_BYTE) {
            // 헤더를 찾았음! 이제 나머지 데이터를 읽는다.
            break;
        } else {
            // 헤더가 아님. 다음 바이트를 계속 확인
            //std::cout << "Skipping byte: 0x" << std::hex << (int)header_buffer[0] << std::dec << std::endl; // Debugging
        }
    }

    // 2. 헤더를 찾았으면, 나머지 20바이트의 데이터를 모두 읽을 때까지 대기한다.
    // read()는 요청한 바이트 수를 모두 읽지 못할 수 있으므로, 루프를 사용
    int total_bytes_read = 0;
    while (total_bytes_read < 20) {
        bytes_read = read(serial_fd, data_buffer + total_bytes_read, 20 - total_bytes_read);
        
        if (bytes_read == 0) { // 타임아웃 또는 데이터가 더 이상 없음
            //std::cerr << "Timeout/No more data while reading remaining packet after header. Only " << total_bytes_read << " bytes received." << std::endl; // Debugging
            return false; // 불완전한 패킷
        }
        if (bytes_read == -1) { // read 에러 발생
            std::cerr << "Error reading serial port for data after header: " << strerror(errno) << std::endl; // Debugging
            return false; // 에러 발생
        }
        total_bytes_read += bytes_read;
    }

    // 3. 읽은 데이터의 길이가 정확히 20바이트인지 확인 (이중 확인, 위의 while 루프가 이미 보장)
    if (total_bytes_read != 20) {
        // 이 부분은 위에 while 루프 때문에 사실상 도달하지 않겠지만, 방어적인 코딩
        // std::cerr << "Incomplete packet after header: expected 20 bytes, got " << total_bytes_read << std::endl; // Debugging
        return false;
    }

    // 4. 수신된 20바이트 데이터를 파싱한다. (빅 엔디안 가정)
    // 파이썬의 `>hhhhhhhhhh`와 동일하게 2바이트씩 10개의 signed short (int16_t)로 해석
    // C++에서 바이트를 int16_t로 변환할 때는 비트 시프트와 OR 연산을 사용 (빅 엔디안)

    // 가속도 데이터 (3 * int16_t)
    accel_x = (int16_t)((data_buffer[0] << 8) | data_buffer[1]);
    accel_y = (int16_t)((data_buffer[2] << 8) | data_buffer[3]);
    accel_z = (int16_t)((data_buffer[4] << 8) | data_buffer[5]);

    // 자이로 데이터 (3 * int16_t)
    gyro_x = (int16_t)((data_buffer[6] << 8) | data_buffer[7]);
    gyro_y = (int16_t)((data_buffer[8] << 8) | data_buffer[9]);
    gyro_z = (int16_t)((data_buffer[10] << 8) | data_buffer[11]);

    // 엔코더 데이터 (4 * uint16_t)
    // 아두이노에서 uint16_t를 보내고 파이썬에서 h (signed short)로 받았으므로,
    // C++에서는 uint16_t로 받는 것이 더 정확하지만, 파이썬 코드의 일관성을 위해 int16_t로 유지합니다.
    // 필요에 따라 uint16_t로 변경 가능합니다.
    encoder1 = (uint16_t)((data_buffer[12] << 8) | data_buffer[13]);
    encoder2 = (uint16_t)((data_buffer[14] << 8) | data_buffer[15]);
    encoder3 = (uint16_t)((data_buffer[16] << 8) | data_buffer[17]);
    encoder4 = (uint16_t)((data_buffer[18] << 8) | data_buffer[19]);

    // 디버깅 출력 (필요시 주석 해제)
    // std::cout << "Accel: X=" << accel_x << ", Y=" << accel_y << ", Z=" << accel_z
    //           << ", Gyro: X=" << gyro_x << ", Y=" << gyro_y << ", Z=" << gyro_z
    //           << ", Encoders: " << encoder1 << ", " << encoder2 << ", " << encoder3 << ", " << encoder4 << std::endl;

    return true; // 데이터 수신 및 파싱 성공
}

bool MRF::openSerial(){

    // Open serial port
    serial_fd = open(serial_port.c_str(), O_RDWR | O_NOCTTY);
    if (serial_fd == -1) {
        std::cerr << "Error opening serial port" << std::endl;
        connected = false;
        return 0;
    }else{
        std::cout << "Serial port opened! "<<  serial_fd  << std::endl;
        connected = true;
    }

    // Configure serial port
    struct termios options;
    tcgetattr(serial_fd, &options);
    cfsetispeed(&options, B115200);
    cfsetospeed(&options, B115200);
    options.c_cflag = CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(serial_fd, TCIFLUSH);
    tcsetattr(serial_fd, TCSANOW, &options);

    return 1;

}

bool MRF::isConnected(){
    return  connected;
}

int16_t MRF::getAccelX(){
    return accel_x;
}

int16_t MRF::getAccelY(){
    return accel_y;
}

int16_t MRF::getAccelZ(){
    return accel_z;
}

int16_t MRF::getGyroX(){
    return gyro_x;
}

int16_t MRF::getGyroY(){
    return gyro_y;
}

int16_t MRF::getGyroZ(){
    return gyro_z;
}

uint16_t MRF::getEncoder1(){
    return encoder1;
}

uint16_t MRF::getEncoder2(){
    return encoder2;
}

uint16_t MRF::getEncoder3(){
    return encoder3;
}

uint16_t MRF::getEncoder4(){
    return encoder4;
}