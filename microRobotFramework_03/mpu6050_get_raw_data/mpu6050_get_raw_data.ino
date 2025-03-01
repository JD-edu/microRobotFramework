// mpu6050_light library install 
#include "Wire.h"
#include <MPU6050_light.h>
#include <SoftwareSerial.h>

#define RX_PIN 7   // Arduino RX
#define TX_PIN 8   // Arduino TX

#define LEFT_MOTOR_PWM 5
#define LEFT_MOTOR_DIR 4
#define RIGHT_MOTOR_PWM 6
#define RIGHT_MOTOR_DIR 7

// We use software seiral for raspberry pi -> arduino motor controlsimulation and debugging  
SoftwareSerial softSerial(RX_PIN, TX_PIN);  // RX, TX

MPU6050 mpu(Wire);

long timer = 0;

/*
packet 
header 0xf5
length
accelX 0
accelX 1
accelY 0
accelY 1
accelZ 0
accelZ 1  
gyroX 0
gyroX 1
gyroY 0
gyroY 1
gyroZ 0
gyroZ 1  
checksum
*/
byte data[23]; 

void setup(){
  Serial.begin(115200);
  softSerial.begin(9600);
  Wire.begin();
  softSerial.println("Motor simulation...");
  byte status = mpu.begin();
  //Serial.print("MPU6050 status: ");
  Serial.println(status);
  pinMode(13, OUTPUT);

  pinMode(LEFT_MOTOR_PWM, OUTPUT);
  pinMode(LEFT_MOTOR_DIR, OUTPUT);
  pinMode(RIGHT_MOTOR_PWM, OUTPUT);
  pinMode(RIGHT_MOTOR_DIR, OUTPUT);

  while(status != 0){
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
    
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
  receiveMotorCommand();
  if(millis() - timer > 50){
    //Serial.println(mpu.getAccX());
    int16_t accelX = (int16_t)(mpu.getAccX()*1000);
    int16_t accelY = (int16_t)(mpu.getAccY()*1000);
    int16_t accelZ = (int16_t)(mpu.getAccZ()*1000);
    int16_t gyroX = (int16_t)(mpu.getGyroX()*1000);
    int16_t gyroY = (int16_t)(mpu.getGyroY()*1000);
    int16_t gyroZ = (int16_t)(mpu.getGyroZ()*1000);
    data[0] = 0xf5;
    data[1] = 21;
    data[2] = (accelX >> 8) & 0xff;
    data[3] = accelX & 0xff;
    data[4] = (accelY >> 8) & 0xff;
    data[5] = accelY & 0xff;
    data[6] = (accelZ >> 8) & 0xff;
    data[7] = accelZ & 0xff;
    data[8] = (gyroX >> 8) & 0xff;
    data[9] = gyroX & 0xff;
    data[10] = (gyroY >> 8) & 0xff;
    data[11] = gyroY & 0xff;
    data[12] = (gyroZ >> 8) & 0xff;
    data[13] = gyroZ & 0xff;
    data[14] = (encoder1 >> 8) & 0xff;
    data[15] = encoder1 & 0xff;
    data[16] = (encoder2 >> 8) & 0xff;
    data[17] = encoder2 & 0xff;
    data[18] = (encoder3 >> 8) & 0xff;
    data[19] = encoder3 & 0xff;
    data[20] = (encoder4 >> 8) & 0xff;
    data[21] = encoder4 & 0xff;
    data[22] = 0;
    Serial.write(data, 23);
    encoder1++; 
    encoder2++;
    encoder3++;
    encoder4++;
    timer = millis();
  }

}

void receiveMotorCommand() {
  if (Serial.available() >= 5) {  // Packet size is 5 bytes
    uint8_t packet[5];
    Serial.readBytes(packet, 5);

    // Verify header (first byte should be 0xAA)
    if (packet[0] != 0xAA) return;

    // Verify checksum
    uint8_t checksum = packet[0] ^ packet[1] ^ packet[2] ^ packet[3];
    //if (checksum != packet[4]) {
    //  softSerial.println("Invalid checksum!");
    //  return;
    //}

    // Extract speed and angle
    int speed = packet[2];       // 0-255 range
    int angle = (int8_t)packet[3]; // Convert to signed int (-127 to 127)

    // Compute left and right motor speeds using differential drive formula
    int left_speed = constrain(speed - (angle / 127.0) * speed, -255, 255);
    int right_speed = constrain(speed + (angle / 127.0) * speed, -255, 255);

    //softSerial.print("Speed: "); softSerial.print(speed);
    //softSerial.print(" Angle: "); softSerial.println(angle);
    softSerial.print(" -> Left Speed: "); softSerial.print(left_speed);
    softSerial.print(" Right Speed: "); softSerial.println(right_speed);

    // Apply motor control
    controlMotors(left_speed, right_speed);
  }
}

void controlMotors(int left_speed, int right_speed) {
  // Left motor control
  if (left_speed > 0) {
    analogWrite(LEFT_MOTOR_PWM, left_speed);
    digitalWrite(LEFT_MOTOR_DIR, HIGH);
  } else {
    analogWrite(LEFT_MOTOR_PWM, -left_speed);
    digitalWrite(LEFT_MOTOR_DIR, LOW);
  }

  // Right motor control
  if (right_speed > 0) {
    analogWrite(RIGHT_MOTOR_PWM, right_speed);
    digitalWrite(RIGHT_MOTOR_DIR, HIGH);
  } else {
    analogWrite(RIGHT_MOTOR_PWM, -right_speed);
    digitalWrite(RIGHT_MOTOR_DIR, LOW);
  }
}
