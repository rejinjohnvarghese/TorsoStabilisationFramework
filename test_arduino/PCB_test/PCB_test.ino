static const uint8_t EN = 8;
static const uint8_t PH  = 37;
static const uint8_t PWM = 38;
static const uint8_t STBY  = 35;
static const uint8_t FAULT  = 36;

void setup() {
  Serial.begin();
  delay (2000);
  // put your setup code here, to run once:
  pinMode(EN, OUTPUT);
  pinMode(PH, OUTPUT);
  pinMode(PWM, OUTPUT);
  pinMode(FAULT, INPUT);
  //pinMode(STBY, OUTPUT);

  digitalWrite(EN, 1);
  //digitalWrite(STBY, 1);
  
  digitalWrite(PH, 0);
  analogWrite(PWM, 255);
  Serial.println("In position 1");
  delay(100);
  
  Serial.println("Disabled");
  analogWrite(EN, 0);
  delay(5000);

  analogWrite(EN, 255);

  // Extend
  digitalWrite(PH, 1);
  analogWrite(PWM, 255);
  Serial.println("In position 2");
  delay(100);

  analogWrite(EN, 0);
  Serial.println("Disabled");
  delay(5000);

  Serial.println("Stop");
  
}

void loop() {
  //Serial.println("Hey");
  //int val = digitalRead(FAULT);
  //Serial.println(val);

}
