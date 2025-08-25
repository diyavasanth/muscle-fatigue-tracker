void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial); // Wait for serial monitor to open

  // Set built-in LED as output
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("Hello BLE Sense! Setup complete.");
}

void loop() {
  // Blink LED
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("LED ON");
  delay(1000);

  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("LED OFF");
  delay(1000);
}
