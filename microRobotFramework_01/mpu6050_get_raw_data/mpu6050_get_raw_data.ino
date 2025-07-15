// mpu6050_light library install 
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

long timer = 0;

// packet structure: header (1byte) + 10 * int16_t (20bytes) = 21 bytes total
// length and checksum fields are not explicitly sent, simplifying the protocol
byte dataBuffer[21]; // Total bytes to send: 1 (header) + 20 (data) = 21 bytes

void setup(){
  Serial.begin(115200);
  Wire.begin();

  byte status = mpu.begin();
  Serial.println(status);
  pinMode(13, OUTPUT);

  while(status != 0){
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
    status = mpu.begin(); // 재시도 로직 추가 (선택 사항)
  }

  Serial.println("Calculation offset. Do not move");
  delay(1000);
  mpu.calcOffsets(true, true);
  Serial.println("Done\n");
}

uint16_t encoder1 = 0;
uint16_t encoder2 = 0;
uint16_t encoder3 = 0;
uint16_t encoder4 = 0;

void loop() {
  mpu.update();
  if(millis() - timer > 50){ // 50ms마다 데이터 전송
    int16_t accelX = (int16_t)(mpu.getAccX()*1000);
    int16_t accelY = (int16_t)(mpu.getAccY()*1000);
    int16_t accelZ = (int16_t)(mpu.getAccZ()*1000);
    int16_t gyroX = (int16_t)(mpu.getGyroX()*1000);
    int16_t gyroY = (int16_t)(mpu.getGyroY()*1000);
    int16_t gyroZ = (int16_t)(mpu.getGyroZ()*1000);

    // Header byte
    dataBuffer[0] = 0xF5; // Header

    // MPU6050 data (6 * int16_t = 12 bytes) - Big-Endian
    dataBuffer[1] = (accelX >> 8) & 0xFF;
    dataBuffer[2] = accelX & 0xFF;
    dataBuffer[3] = (accelY >> 8) & 0xFF;
    dataBuffer[4] = accelY & 0xFF;
    dataBuffer[5] = (accelZ >> 8) & 0xFF;
    dataBuffer[6] = accelZ & 0xFF;
    dataBuffer[7] = (gyroX >> 8) & 0xFF;
    dataBuffer[8] = gyroX & 0xFF;
    dataBuffer[9] = (gyroY >> 8) & 0xFF;
    dataBuffer[10] = gyroY & 0xFF;
    dataBuffer[11] = (gyroZ >> 8) & 0xFF;
    dataBuffer[12] = gyroZ & 0xFF;

    // Encoder data (4 * uint16_t = 8 bytes) - Big-Endian
    dataBuffer[13] = (encoder1 >> 8) & 0xFF;
    dataBuffer[14] = encoder1 & 0xFF;
    dataBuffer[15] = (encoder2 >> 8) & 0xFF;
    dataBuffer[16] = encoder2 & 0xFF;
    dataBuffer[17] = (encoder3 >> 8) & 0xFF;
    dataBuffer[18] = encoder3 & 0xFF;
    dataBuffer[19] = (encoder4 >> 8) & 0xFF;
    dataBuffer[20] = encoder4 & 0xFF;
    
    // Total 1 (header) + 20 (data) = 21 bytes sent
    Serial.write(dataBuffer, 21); // Send 21 bytes

    encoder1++; 
    encoder2++;
    encoder3++;
    encoder4++;
    timer = millis();
  }
}