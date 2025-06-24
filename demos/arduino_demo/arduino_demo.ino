#include "BLEDevice.h"          // BLE library
#include <Adafruit_LSM6DSOX.h>  // LSM6DSOX IMU library 

// Solenoid driver pins
static const uint8_t EN = 8;
static const uint8_t PH  = 37;
static const uint8_t PWM = 38;
static const uint8_t STBY  = 35;
static const uint8_t FAULT  = 36;

// BLE service and characteristics
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = true;
bool oldDeviceConnected = false;
uint32_t value = 0;

// For the LSM6DSOX IMU
Adafruit_LSM6DSOX sox;

float threshold = 8.1;
unsigned long int start_time_on;
bool threshold_reached = false; 
float release_time = 10.0;
bool solenoid_status = 0;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
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
    while (1) {
      delay(10);
    }
  }
  sox.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  sox.setAccelDataRate(LSM6DS_RATE_416_HZ);

  // Initialize BLE module
  BLEDevice::init("ESP32 IMU");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  //pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create the BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_INDICATE
                    );


  pCharacteristic->setValue("First test value");
  pService->start();
  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x0);  
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");

  // Retracted
  digitalWrite(EN, 1);
  digitalWrite(PH, 0);
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
  if ((acc_mag < threshold) && (!threshold_reached)) {
    threshold_reached = true;
    solenoid_status = 1;
    digitalWrite(LED_BUILTIN, HIGH);

    // Extend solenoid 
    digitalWrite(EN, 1);
    digitalWrite(PH, 1);
    analogWrite(PWM, 255);
    delay(100);
    digitalWrite(EN, 0);

    start_time_on = millis();
  }

  String dataString = String(timestamp) + ","
                  + String(accel.acceleration.x) + ","
                  + String(accel.acceleration.y) + ","
                  + String(accel.acceleration.z) + ","
                  + String(solenoid_status);
  

  pCharacteristic->setValue(dataString.c_str());
  pCharacteristic->notify();

  if (((millis()-start_time_on) > (release_time*1000)) & (threshold_reached)) {
    threshold_reached = false;
    digitalWrite(LED_BUILTIN, LOW);
    solenoid_status = 0;
        
    // Retract solenoid 
    digitalWrite(EN, 1);
    digitalWrite(PH, 0);
    analogWrite(PWM, 255);
    Serial.println("Retract impulse");
    delay(100);
    digitalWrite(EN, 0);
  }

}

