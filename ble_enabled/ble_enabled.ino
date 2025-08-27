#include <ArduinoBLE.h>
#include <Arduino_BMI270_BMM150.h>  // IMU sensor

// Fixed UUIDs (random but constant)
#define IMU_SERVICE_UUID       "12345678-1234-5678-1234-56789abcdef0"
#define IMU_CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"

BLEService imuService(IMU_SERVICE_UUID);
BLECharacteristic imuChar(IMU_CHARACTERISTIC_UUID, BLERead | BLENotify, 100);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("BLE_Fatigue_Tracker");
  BLE.setAdvertisedService(imuService);

  imuService.addCharacteristic(imuChar);
  BLE.addService(imuService);

  imuChar.writeValue("IMU ready");

  BLE.advertise();
  Serial.println("✅ BLE IMU Service advertising...");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    while (central.connected()) {
      float ax, ay, az, gx, gy, gz, mx, my, mz;

      if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && IMU.magneticFieldAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        IMU.readGyroscope(gx, gy, gz);
        IMU.readMagneticField(mx, my, mz);

        char buffer[100];
        snprintf(buffer, sizeof(buffer), "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f",
                 ax, ay, az, gx, gy, gz, mx, my, mz);

        imuChar.writeValue(buffer);
        Serial.println(buffer);
      }

      delay(100); // ~10 Hz
    }

    Serial.println("Disconnected");
  }
}
