#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Adafruit_LSM6DSOX.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

Adafruit_LSM6DSOX sox;

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = true;
bool oldDeviceConnected = false;
uint32_t value = 0;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

void setup() {
  // Delay to see the Serial prints
  delay(1000);

  Serial.begin(115200);
  Serial.println("Starting BLE work!");

  // Initialize the sensorS
  if (!sox.begin_I2C()) {   
    Serial.println("Failed to find LSM6DSOX chip");
    while (1) {
      delay(10);
    }
  }

  sox.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  sox.setAccelDataRate(LSM6DS_RATE_12_5_HZ);

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
}

void loop() {

  // Get new sensor events
  sensors_event_t accel, gyro, temp;
  sox.getEvent(&accel, &gyro, &temp);  

  unsigned long timestamp = millis();

  String dataString = String(timestamp) + ","
                  + String(accel.acceleration.x) + ","
                  + String(accel.acceleration.y) + ","
                  + String(accel.acceleration.z);

  //pCharacteristic->setValue((uint8_t*)&value, 4);
  pCharacteristic->setValue(dataString.c_str());
  pCharacteristic->notify();
  //value++;
  delay(3); // bluetooth stack will go into congestion, if too many packets are sent, in 6 hours test i was able to go as low as 3ms

}