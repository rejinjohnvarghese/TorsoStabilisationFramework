import socket
import pandas as pd
import matplotlib.pyplot as plt
import time
from drawnow import drawnow, figure
from matplotlib.animation import FuncAnimation

# Load and downsample the data
#data_path = "../LSTM_3_classes/test_data/0.80_processed_real_time.csv"
data_path = "../Trash/LSTM_3_classes/test_data/0.80_processed_real_time.csv"

data = pd.read_csv(data_path)
data_downsampled = data.iloc[::4, :]  # Downsample the data to 50Hz

# Setup initial figure and plot
#fig, ax = plt.subplots()
#line, = ax.plot([], [], 'r-')
#ax.set_ylim(0, 30)   # Adjust these limits based on your expected data

#figure()
#x, y = [], []
#line, = ax.plot(x, y)

def init():
    """Initialize the background of the animation."""
    line.set_data([], [])
    return line,

def update():
    global x,y
    """Update the plot with new data."""
    # 'frame' could be unused if you're fetching global data
    #xdata.append(frame[0])
    #ydata.append(frame[1])
    xdata = x[-20:]  # Keep last 20 points for a sliding window effect
    ydata = y[-20:]
    line.set_data(xdata, ydata)
    
    # Optionally adjust limits dynamically here if needed
    #return line,

def update_plot(new_x, new_y):
    global x, y, line, ax
    x.append(new_x)
    y.append(new_y)
    
    # Keep only the last 20 data points for a sliding window effect
    x = x[-20:]
    y = y[-20:]

    # Update line data
    line.set_xdata(x)
    line.set_ydata(y)
    
    # Adjust x-axis limits dynamically based on the new data
    ax.set_xlim(min(x), max(x) + 10)  # Adjust as needed

    # Adjust y-axis limits if necessary (optional)
    #ax.set_ylim(0, max(y) + 5)  # Adjust as needed for your data range
    ax.set_ylim(0,30)
    
    # Redraw the plot
    ax.figure.canvas.draw()
    ax.figure.canvas.flush_events()

# Setup socket for sending data
host = 'localhost'
port = 12345
start_time = time.time()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print("Waiting for a connection...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        for index, row in data_downsampled.iterrows():
            # Format data string with acceleration_mag and acceleration_z
            data_str = f"{row['acceleration_magnitude']},{row['acceleration_z']}\n"
            #print(data_str)
            conn.sendall(data_str.encode('utf-8'))
            
            # Update plot with new data
            print(time.time()-start_time)
            start_time = time.time()
           
            time.sleep(1/20)  # Simulate 50Hz frequency
        print("Data transmission complete.")