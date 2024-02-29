// Pin number where the LED is connected
const int ledPin = 2;

void setup()
{
  // Initialize the LED pin as an output
  pinMode(ledPin, OUTPUT);
}

void loop()
{
  // Turn the LED on (HIGH) for 1 second
  digitalWrite(ledPin, HIGH);
  delay(1000);

  // Turn the LED off (LOW) for 1 second
  digitalWrite(ledPin, LOW);
  delay(1000);
}
