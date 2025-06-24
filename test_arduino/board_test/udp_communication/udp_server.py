import socket
import time

UDP_IP = "192.168.1.185" # The IP that is printed in the serial monitor from the ESP32
SHARED_UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.connect((UDP_IP, SHARED_UDP_PORT))

def loop():
    while True:

        #data = sock.recv(2048)
        #print(data)

        start_time = time.time()
        data = sock.recv(2048)
        end_time = time.time()

        elapsed_time = end_time - start_time
        if elapsed_time > 0:
            frequency = 1 / elapsed_time
        else:
            frequency = 0

        print(f"Data: {data}, Frequency: {frequency:.2f} Hz")

if __name__ == "__main__":
    try:
        sock.sendto('Hello ESP32'.encode(), (UDP_IP, SHARED_UDP_PORT))
        loop()
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()
        print("Socket closed")