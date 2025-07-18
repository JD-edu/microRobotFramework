void setup() {
    Serial.begin(115200);  // Initialize Serial at 115200 baud rate
    randomSeed(analogRead(0)); // Seed random number generator
}

void loop() {
    float accelX = random(-1000, 1000) / 1000.0;  // Simulated raw X acceleration
    float accelY = random(-1000, 1000) / 1000.0;  // Simulated raw Y acceleration
    float accelZ = random(-1000, 1000) / 1000.0;  // Simulated raw Z acceleration

    // Convert float data to byte array
    byte buffer[12]; 
    memcpy(buffer, &accelX, 4);
    memcpy(buffer + 4, &accelY, 4);
    memcpy(buffer + 8, &accelZ, 4);

    // Send as raw binary data
    Serial.write(buffer, 12); 

    delay(100); // Delay 100ms to simulate real sensor output rate
}
