#include <Arduino_BMI270_BMM150.h>

void setup() {
  Serial.begin(115200);
  while (!Serial);

  // Initialize IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("X\tY\tZ\t| Roll\tPitch\tYaw");
}

void loop() {
  float ax, ay, az;  // accelerometer
  float gx, gy, gz;  // gyroscope
  float mx, my, mz;  // magnetometer (for yaw/orientation)

  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && IMU.magneticFieldAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);
    IMU.readMagneticField(mx, my, mz);

    // ---- Simple orientation estimation ----
    float roll  = atan2(ay, az) * 180 / PI;
    float pitch = atan(-ax / sqrt(ay * ay + az * az)) * 180 / PI;
    float yaw   = atan2(my, mx) * 180 / PI;  // crude heading

    // Print values
    Serial.print(ax); Serial.print("\t");
    Serial.print(ay); Serial.print("\t");
    Serial.print(az); Serial.print("\t|\t");
    Serial.print(roll); Serial.print("\t");
    Serial.print(pitch); Serial.print("\t");
    Serial.println(yaw);
  }
}
