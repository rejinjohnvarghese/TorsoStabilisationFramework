const int analogPin = T5; 
int potValue = 0;

void setup() {
  Serial.begin(115200);

}

void loop() {
  potValue = analogRead(analogPin);

  Serial.println("Potentiometer Value: ");
  Serial.println(potValue);
  
  delay(100); // Short delay to make the output readable

}
