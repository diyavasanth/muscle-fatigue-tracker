#include <Wire.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  byte status = mpu.begin();
  Serial.print("MPU6050 status: ");
  Serial.println(status);
  // status = 0 means OK

  if (status != 0) {
    Serial.println("Sensor failed to initialize. Check wiring and power.");
    while (1);
  }

  Serial.println("Calibrating...");
  delay(1000);
  mpu.calcOffsets(); // auto-calibrate
  Serial.println("Calibration complete.");
}

void loop() {
  mpu.update();

  Serial.print("Accel (g) X: ");
  Serial.print(mpu.getAccX());
  Serial.print(" | Y: ");
  Serial.print(mpu.getAccY());
  Serial.print(" | Z: ");
  Serial.println(mpu.getAccZ());

  Serial.print("Gyro (°/s) X: ");
  Serial.print(mpu.getGyroX());
  Serial.print(" | Y: ");
  Serial.print(mpu.getGyroY());
  Serial.print(" | Z: ");
  Serial.println(mpu.getGyroZ());

  Serial.println("-----------------------------");
  delay(500);
}
