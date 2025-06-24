#include "BLEDevice.h"          // BLE library
#include <Adafruit_LSM6DSOX.h>  // LSM6DSOX IMU library 

// Solenoid driver pins
static const uint8_t EN = 8;
static const uint8_t PH  = 37;
static const uint8_t PWM = 38;
static const uint8_t STBY  = 35;
static const uint8_t FAULT  = 36;

// BLE service and characteristics
#define SERVICE_UUID                      "A07498CA-AD5B-474E-940D-16F1FBE7E8CD" 
#define THRESHOLD_CHARACTERISTIC_UUID     "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"
#define STATUS_CHARACTERISTIC_UUID        "54855A27-E740-479B-B202-95ED22B1D437"
#define RELEASE_TIME_CHARACTERISTIC_UUID  "30DDCD11-45FC-4A90-BD3D-83C969F48ADF"

// Variable for BLE
BLEServer *pServer = nullptr;
BLECharacteristic *pThresholdCharacteristic = nullptr;
BLECharacteristic *pStatusCharacteristic = nullptr;
BLECharacteristic *pReleaseTimeCharacteristic = nullptr;

// For the LSM6DSOX IMU
Adafruit_LSM6DSOX sox;

// General variables 
float threshold = 8.0;
unsigned long int start_time_on;
bool threshold_reached = false; 
float release_time = 5.0;

// Callback when a message is received from the smartphone (either threshold or release time)
class MyCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) override {
        std::string value = pCharacteristic->getValue();

        if (value.length() == sizeof(float)) {
            const char *pValue = value.c_str(); 

            if (pCharacteristic == pThresholdCharacteristic) {
                memcpy(&threshold, pValue, sizeof(threshold));
                Serial.print("Threshold updated to: ");
                Serial.println(threshold);
            } 
            else if (pCharacteristic == pReleaseTimeCharacteristic) {
                memcpy(&release_time, pValue, sizeof(release_time));
                Serial.print("Release time updated to: ");
                Serial.println(release_time);
            }
        } else {
            Serial.println("Received value of unexpected size.");
        }
    }
};

void setup() {
  Serial.begin();
  delay (2000);

  // Configure the LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  // Configure the solenoid driver pins
  pinMode(EN, OUTPUT);
  pinMode(PH, OUTPUT);
  pinMode(PWM, OUTPUT);
  //pinMode(FAULT, INPUT);
  //pinMode(STBY, OUTPUT);

  // Initialize the sensors
  if (!sox.begin_I2C()) {   
  //if (!sox.begin_I2C(LSM6DS_I2CADDR_DEFAULT, &Wire1)) {  
    Serial.println("Failed to find LSM6DSOX chip");
    while (1) {
      delay(10);
    }
  }
  sox.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  sox.setAccelDataRate(LSM6DS_RATE_416_HZ);

  // Initialize BLE module
  Serial.println("Starting Arduino BLE Client application...");
  BLEDevice::init("Torso Stabiliser");
  pServer = BLEDevice::createServer();

  BLEService *pService = pServer->createService(SERVICE_UUID);
  pThresholdCharacteristic = pService->createCharacteristic(
                      THRESHOLD_CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_WRITE);
  pStatusCharacteristic = pService->createCharacteristic(
                          STATUS_CHARACTERISTIC_UUID,
                          BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
  pReleaseTimeCharacteristic = pService->createCharacteristic(
                      RELEASE_TIME_CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_WRITE);
  pService->start();

  pServer->getAdvertising()->start();
  Serial.println("Waiting for a client connection to notify...");
  BLEAddress bleAddress = BLEDevice::getAddress();
  Serial.print("BLE Address: ");
  Serial.println(bleAddress.toString().c_str());

  pThresholdCharacteristic->setCallbacks(new MyCallbacks());
  pReleaseTimeCharacteristic->setCallbacks(new MyCallbacks());

  // Retract the solenoid 
  digitalWrite(EN, 1);
  digitalWrite(PH, 0);
  analogWrite(PWM, 255);
  Serial.println("Retracted");
  delay(100);
  digitalWrite(EN, 0);
  
}

void loop() {

  // Get new sensor events
  sensors_event_t accel, gyro, temp;
  sox.getEvent(&accel, &gyro, &temp);  

  // Get the timestamp
  unsigned long timestamp = millis();

  // Threshold trigger
  float acc_mag = sqrt(pow(accel.acceleration.x, 2) + pow(accel.acceleration.y, 2) + pow(accel.acceleration.z, 2));
  //Serial.println(acc_mag);
  if ((acc_mag < threshold) && (!threshold_reached)) {

    threshold_reached = true;
    digitalWrite(LED_BUILTIN, HIGH);

    Serial.println(acc_mag);

    // Extend solenoid 
    digitalWrite(EN, 1);
    digitalWrite(PH, 1);
    analogWrite(PWM, 255);
    Serial.println("Extend impulse");
    delay(100);
    digitalWrite(EN, 0);
    Serial.println("Disabled");
    updateSolenoidStatus(true);

    start_time_on = millis();
    String dataString = String(timestamp) + ","
                  + String(accel.acceleration.x) + ","
                  + String(accel.acceleration.y) + ","
                  + String(accel.acceleration.z);

  }

  // Retract the solenoid based on the release_time value 
  if (((millis()-start_time_on) > (release_time*1000)) & (threshold_reached)) {
    threshold_reached = false;
    digitalWrite(LED_BUILTIN, LOW);
        
    // Retract solenoid 
    digitalWrite(EN, 1);
    digitalWrite(PH, 0);
    analogWrite(PWM, 255);
    Serial.println("Retract impulse");
    delay(100);
    digitalWrite(EN, 0);
    Serial.println("Disabled");
    updateSolenoidStatus(false);
  }

}

// Send the solenoid status to the smartphone (to display on the app)
void updateSolenoidStatus(bool isExtended) {
    uint8_t status = isExtended ? 1 : 0;
    pStatusCharacteristic->setValue(&status, 1);
    pStatusCharacteristic->notify(); 
}

