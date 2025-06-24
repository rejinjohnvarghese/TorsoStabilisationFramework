// Arduino
//#define ENABLE 5
//#define DIRA 3
//#define DIRB 4

//ESP32
#define ENABLE 18
#define DIRA 16
#define DIRB 17
 
void setup() {
  delay (2000);
  //---set pin direction
  pinMode(ENABLE,OUTPUT);
  pinMode(DIRA,OUTPUT);
  pinMode(DIRB,OUTPUT);
  Serial.begin(115200);
  Serial.println("Start");

  analogWrite(ENABLE, 255);
  
  // Retract
  digitalWrite(DIRA, 0);
  digitalWrite(DIRB, 1);
  Serial.println("In position 1");
  delay(100);

  Serial.println("Disabled");
  analogWrite(ENABLE, 0);
  delay(5000);

  analogWrite(ENABLE, 255);

  // Extend
  digitalWrite(DIRA, 1);
  digitalWrite(DIRB, 0);
  Serial.println("In position 2");
  delay(100);

  analogWrite(ENABLE, 0);
  Serial.println("Disabled");
  delay(5000);

  Serial.println("Stop");
  
}

void loop() {

}
   
