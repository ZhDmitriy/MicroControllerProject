#define LED_GREEN 8
#define LED_RED 9

void setup() {
  Serial.begin(9600);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
}

void loop() {

  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');

    Serial.println(msg);

    if (msg == "SUCCESS") {
      digitalWrite(LED_GREEN, HIGH);
      digitalWrite(LED_RED, LOW);
      delay(15000);
    } else if (msg == "FAILED") {
      digitalWrite(LED_RED, HIGH);
      digitalWrite(LED_GREEN, LOW);
      delay(15000);
    }
  } else {
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, LOW);
  }

}
