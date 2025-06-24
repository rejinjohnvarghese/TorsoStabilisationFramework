import asyncio
from bleak import BleakScanner, BleakClient, BleakError
from datetime import datetime

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

NUMBER = '1.00'

# Get the current date and time
now = datetime.now()
formatted_date = now.strftime("%Y_%m_%d_%H_%M_%S")

# Open or create the CSV file to store data with a filename including the date and time
filename = f"raw/{NUMBER}_raw.csv"
# Open or create the CSV file to store data
with open(filename, mode='w', newline='') as file:
    # Writing header to the CSV file
    file.write("timestamp,acceleration_x,acceleration_y,acceleration_z\n")
        

def notification_handler(sender, data):
    """Handles incoming notifications."""
    # Convert bytes to string
    data_string = data.decode('utf-8')
    
    # Split the string by commas to separate the values
    values = data_string.split(',')
    
    # You can then access individual values by indexing the 'values' list
    #timestamp = values[0]
    #accel_x = values[1]
    #accel_y = values[2]
    #accel_z = values[3]

    with open(filename, mode='a', newline='') as file:
        file.write(f"{values[0]},{values[1]},{values[2]},{values[3]}\n")
        file.flush()  # Ensure that data is written to the disk        
    
    # Print the received values
    #print(f"Timestamp: {timestamp}")
    #print(f"Acceleration X: {accel_x}")
    #print(f"Acceleration Y: {accel_y}")
    #print(f"Acceleration Z: {accel_z}")

async def run():
    devices = await BleakScanner.discover()
    ESP32_device = None
    
    for device in devices:
        if device.name == "ESP32 IMU" :  # Adjust the name based on your ESP32 device name
            ESP32_device = device
            #async with BleakClient(ESP32_device) as client:
            #    value = await client.read_gatt_char(CHARACTERISTIC_UUID)
            #    print(f"Characteristic Value: {value.decode('utf-8')}")
            break
    
    if ESP32_device:
        client = BleakClient(ESP32_device)
        try:
            await client.connect()
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            print("Connected and waiting for notifications...")
            await asyncio.sleep(9999)  # Keep alive for receiving notifications
        except BleakError as e:
            print(e)
        finally:
            await client.stop_notify(CHARACTERISTIC_UUID)
            await client.disconnect()
    else:
        print("ESP32 IMU device not found!")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


