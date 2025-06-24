#include <Adafruit_LSM6DSOX.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789

// For the LSM6DSOX IMU
Adafruit_LSM6DSOX sox;
// For 1.14", 1.3", 1.54", 1.69", and 2.0" TFT with ST7789:
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  
  // Initialize the sensors
  if (!sox.begin_I2C()) {   
    Serial.println("Failed to find LSM6DSOX chip");
    while (1) {
      delay(10);
    }
  }

  sox.setAccelRange(LSM6DS_ACCEL_RANGE_4_G);
  sox.setAccelDataRate(LSM6DS_RATE_104_HZ);

  // Initialize the TFT screen
  // Init ST7789 240x135
  tft.init(135, 240);           
  // turn on backlite
  pinMode(TFT_BACKLITE, OUTPUT);
  digitalWrite(TFT_BACKLITE, HIGH);
  // Put a black background
  tft.fillScreen(ST77XX_BLACK);
  // Set the fontsize
  tft.setTextSize(3);
  // Landscape orientation
  tft.setRotation(3);

}

void loop() {
  // Get new sensor events
  sensors_event_t accel, gyro, temp;
  sox.getEvent(&accel, &gyro, &temp);  

  // Get the timestamp
  unsigned long timestamp = millis();

  // Screen refresh
  tft.setTextColor(ST77XX_WHITE, ST77XX_BLACK);

  // Display on the screen
  tft.setCursor(0, 0);
  tft.println("Acceleration:");
  tft.print("X: ");
  tft.println(accel.acceleration.x);
  //tft.println(" m/s^2");
  
  tft.print("Y: ");
  tft.println(accel.acceleration.y);
  //tft.println(" m/s^2");
  
  tft.print("Z: ");
  tft.println(accel.acceleration.z);
  //tft.println(" m/s^2");

  delay(100); // Update every 500ms

}
