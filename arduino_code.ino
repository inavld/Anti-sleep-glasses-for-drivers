// Pin definitions
const int irSensorPin = 2;   // IR sensor OUT connected to D2
const int buzzerPin = 3;     // Buzzer S connected to D3

void setup() {
  Serial.begin(9600);
  pinMode(irSensorPin, INPUT);     // Set IR sensor as input
  pinMode(buzzerPin, OUTPUT);      // Set buzzer as output
  digitalWrite(buzzerPin, LOW);    // Start with buzzer off
  Serial.println("Setup complete. Monitoring eye status...");
}

void loop() {
  int sensorValue = digitalRead(irSensorPin); // Read IR sensor

  if (sensorValue == LOW) {
    // Eyes closed (IR detects object)
    digitalWrite(buzzerPin, HIGH);  // Turn buzzer ON
    Serial.println("CLOSED");
  } else {
    // Eyes open (no detection)
    digitalWrite(buzzerPin, LOW);   // Turn buzzer OFF
    Serial.println("OPEN");
  }

  delay(50); // Small delay to prevent flicker
}
