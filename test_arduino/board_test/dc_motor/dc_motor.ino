//www.elegoo.com
//2016.12.12

/************************
Exercise the motor using
the L293D chip
************************/

#define ENABLE 18
#define DIRA 16
#define DIRB 17

int i;
 
void setup() {
  //---set pin direction
  pinMode(ENABLE,OUTPUT);
  pinMode(DIRA,OUTPUT);
  pinMode(DIRB,OUTPUT);
  Serial.begin(115200);
}

void loop() {
  delay(2000);
  Serial.println("Moving");
  analogWrite(ENABLE, 200);
  digitalWrite(DIRA, LOW);
  digitalWrite(DIRB, HIGH);
  delay(500);
  Serial.println("Stop");
  digitalWrite(DIRB, LOW);
}
   