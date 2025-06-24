#include <Adafruit_LSM6DSOX.h>  // LSM6DSOX IMU library 

// Solenoid driver pins
static const uint8_t EN = 8;
static const uint8_t PH  = 37;
static const uint8_t PWM = 38;
static const uint8_t STBY  = 35;
static const uint8_t FAULT  = 36;

// For the LSM6DSOX IMU
Adafruit_LSM6DSOX sox;

bool data_for_graph = false;
bool debug = false;
float threshold = 8.0;
unsigned long int start_time_on;
bool threshold_reached = false; 
float release_time = 5.0;

// Interrupt pin for the button
const int buttonPin = A0; // Change this to your interrupt pin
volatile bool solenoidExtended = false;
volatile unsigned long endTime = 0;

void solenoidExtendedISR() {
  solenoidExtended = true;
  //endTime = millis();
  endTime = micros();
}

void setup() {
  Serial.begin();
  delay (2000);

  // Configure the LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  // Configure the button pins
  pinMode(buttonPin, INPUT_PULLUP); // Enable internal pull-up resistor
  attachInterrupt(digitalPinToInterrupt(buttonPin), solenoidExtendedISR, FALLING); // Trigger on FALLING signal

  // Configure the solenoid driver pins
  pinMode(EN, OUTPUT);
  pinMode(PH, OUTPUT);
  pinMode(PWM, OUTPUT);
  //pinMode(FAULT, INPUT);
  //pinMode(STBY, OUTPUT);

  // Initialize the sensors
  if (!sox.begin_I2C()) {   
    if (debug){ 
      Serial.println("Failed to find LSM6DSOX chip");
    }
    while (1) {
      delay(10);
    }
  }
  sox.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  sox.setAccelDataRate(LSM6DS_RATE_416_HZ);

  // Retracted
  digitalWrite(EN, 1);
  digitalWrite(PH, 0);
  analogWrite(PWM, 255);
  delay(100);
  digitalWrite(EN, 0);
  //updateSolenoidStatus(false);
  
}

void loop() {

  // Get new sensor events
  sensors_event_t accel, gyro, temp;
  sox.getEvent(&accel, &gyro, &temp);  

  // Get the timestamp
  unsigned long timestamp = millis();

  // Threshold trigger
  float acc_mag = sqrt(pow(accel.acceleration.x, 2) + pow(accel.acceleration.y, 2) + pow(accel.acceleration.z, 2));
  if ((acc_mag < threshold) && (!threshold_reached)) {
  //if ((accel.acceleration.z > threshold) || (accel.acceleration.x > threshold) || (accel.acceleration.y > threshold)){
    //start_time_on = millis();
    start_time_on = micros();
    threshold_reached = true;
    digitalWrite(LED_BUILTIN, HIGH);
    if (debug){
      Serial.println(acc_mag);
    }

    // Extend solenoid 
    digitalWrite(EN, 1);
    digitalWrite(PH, 1);
    analogWrite(PWM, 255);
    if (debug){
      Serial.println("Extend impulse");
    }
    delay(100);
    digitalWrite(EN, 0);
    if (debug){
      Serial.println("Disabled");
    }

    String dataString = String(timestamp) + ","
                  + String(accel.acceleration.x) + ","
                  + String(accel.acceleration.y) + ","
                  + String(accel.acceleration.z);
    if (data_for_graph){
      Serial.println(dataString);
    }
  }

  if (solenoidExtended) {
    unsigned long duration = endTime - start_time_on;
    Serial.print("Duration: ");
    Serial.print(duration);
    Serial.println(" microseconds");
    delay(1000);
    solenoidExtended = false;
  }

  if (((millis()-start_time_on) > (release_time*1000)) & (threshold_reached)) {
    threshold_reached = false;
    digitalWrite(LED_BUILTIN, LOW);
        
    // Retract solenoid 
    digitalWrite(EN, 1);
    digitalWrite(PH, 0);
    analogWrite(PWM, 255);
    Serial.println("Retract impulse");
    delay(50);
    digitalWrite(EN, 0);
    if (debug){
      Serial.println("Disabled");
    }
  }

}


