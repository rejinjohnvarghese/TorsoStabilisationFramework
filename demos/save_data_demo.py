import asyncio
import aioconsole
from bleak import BleakScanner, BleakClient, BleakError
from datetime import datetime
import threading
import cv2
import signal
import struct

SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#SERVICE_UUID = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD" 
THRESHOLD_CHARACTERISTIC_UUID = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"
NUMBER = 'C.00'

# Get the current date and time
now = datetime.now()
formatted_date = now.strftime("%Y_%m_%d_%H_%M_%S")

# Filename for the CSV and video
filename_csv = f"{NUMBER}_raw_full.csv"
filename_video = f"{NUMBER}_video.avi"

# Open the CSV file to store data
with open(filename_csv, mode='w', newline='') as file:
    file.write("timestamp,acceleration_x,acceleration_y,acceleration_z,solenoid_status\n")

class VideoRecorder:
    def __init__(self, filename):
        self.filename = filename
        self.recording = False
        self.cap = cv2.VideoCapture(0)
        # Check and adjust this frame rate
        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS) 
        self.out = None
        self.thread = None

    def start_recording(self):
        if not self.cap.isOpened():
            print("Error: Camera not accessible")
            return

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # Use the frame rate obtained from the camera
        self.out = cv2.VideoWriter(self.filename, fourcc, self.frame_rate, (640, 480))
        self.recording = True

        while self.recording:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)
            else:
                break

    def stop_recording(self):
        self.recording = False
        if self.out is not None:
            self.out.release()
            self.out = None
        if self.cap.isOpened():
            self.cap.release()

    def run(self):
        self.thread = threading.Thread(target=self.start_recording)
        self.thread.start()

    def join(self):
        if self.thread:
            self.thread.join()

def notification_handler(sender, data):
    """Handles incoming notifications."""
    #if not video_recorder.recording:
    #    video_recorder.run()
    # Convert bytes to string
    data_string = data.decode('utf-8')
    
    # Split the string by commas to separate the values
    values = data_string.split(',')
    
    # You can then access individual values by indexing the 'values' list
    #timestamp = values[0]
    #accel_x = values[1]
    #accel_y = values[2]
    #accel_z = values[3]

    # Ensure there are 9 values (for timestamp, 3 each from accel, gyro, and magnetometer)
    if len(values) != 5:
        print(f"Received data: {data_string}")
        #print("Incorrect data format received")
        return

    with open(filename_csv, mode='a', newline='') as file:
        file.write(f"{values[0]},{values[1]},{values[2]},{values[3]},{values[4]}\n")
        file.flush()  # Ensure that data is written to the disk     
    
    #print(f"Received data: {data_string}")

    
    # Print the received values
    #print(f"Timestamp: {timestamp}")
    #print(f"Acceleration X: {accel_x}")
    #print(f"Acceleration Y: {accel_y}")
    #print(f"Acceleration Z: {accel_z}")

async def run(video_recorder):
    devices = await BleakScanner.discover()
    ESP32_device = None

    for device in devices:
        if device.name == "ESP32 IMU":  # Adjust the name based on your ESP32 device name
            ESP32_device = device
            break

    if ESP32_device:
        client = BleakClient(ESP32_device)
        try:
            await client.connect()
            print("Connected to ESP32. Press Enter to start recording and data collection.")
            await aioconsole.ainput("Press Enter to continue...")  # Wait for user input

            # Now start video recording
            #video_recorder.run()

            # Start notification handler
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            print("Recording and data collection started...")

            # Keep alive for receiving notifications
            await asyncio.sleep(9999)

        except BleakError as e:
            print(e)
        finally:
            await client.stop_notify(CHARACTERISTIC_UUID)
            await client.disconnect()
    else:
        print("ESP32 IMU device not found!")

def signal_handler(sig, frame, video_recorder, loop):
    print('Stopping...')

    # Stop the video recording
    #video_recorder.stop_recording()

    for task in asyncio.all_tasks(loop):
        task.cancel()

    # Stop the asyncio event loop

    loop.call_soon_threadsafe(loop.stop)


if __name__ == "__main__":
    video_recorder = VideoRecorder(filename_video)
    loop = asyncio.get_event_loop()

    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, video_recorder, loop))

    try:
        loop.run_until_complete(run(video_recorder))
    except RuntimeError as e:
        # Handle the RuntimeError raised when stopping the loop
        print("RuntimeError: ", e)
    finally:
        # Ensure the video recorder is properly stopped
        #video_recorder.join()
        loop.close()