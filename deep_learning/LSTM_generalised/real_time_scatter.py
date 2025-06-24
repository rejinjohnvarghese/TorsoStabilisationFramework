import socket
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import time

# Setup socket for receiving data
host = 'localhost'
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Load model
model = load_model('../LSTM/50Hz/model_200ep_32units_50Hz.h5')

# Normalization values
acc_mag_mean = 9.958831727261767
acc_mag_std = 0.6981325300451422
acc_z_mean = 7.875712086220169
acc_z_std = 3.210137793501823

window_size = 25

def normalize_data(value, mean, std):
    return (value - mean) / std

def predict_from_buffer(buffer, model):
    np_buffer = np.array(buffer)
    normalized_mag = normalize_data(np_buffer[:, 0], acc_mag_mean, acc_mag_std)
    normalized_z = normalize_data(np_buffer[:, 1], acc_z_mean, acc_z_std)
    model_input = np.stack((normalized_mag, normalized_z), axis=-1).reshape(1, len(buffer), 2)
    prediction = model.predict(model_input, verbose=1)
    return np.argmax(prediction, axis=1)[0]

# Function to return color based on prediction
def get_color(prediction):
    if prediction == 0:
        return 'green'  # No fall
    elif prediction == 1:
        return 'orange'  # Pre fall
    elif prediction == 2:
        return 'red'  # Fall

predictions = []
colors = []

# Create figure for plotting
plt.ion()
fig, ax = plt.subplots()
ax.set_ylim([0, 30])
plt.setp(ax.get_xticklabels(), visible=False)

def animate():
    sc.set_offsets(np.c_[xs, ys[-20:]])  # Update positions to last 20 Y values
    sc.set_color(colors[-20:])  # Update colors to last 20 colors
    plt.draw()
    plt.pause(0.001)

x_len = 20
xs = list(range(x_len))
ys = [0] * x_len


# Initialize scatter plot
sc = ax.scatter(xs, ys, s=40)

start_time = time.time()

try:
    data_buffer = ""
    data_list = []
    while True:
        data = s.recv(1024).decode('utf-8')
        if not data:
            break
        data_buffer += data
        while '\n' in data_buffer:
            line, data_buffer = data_buffer.split('\n', 1)
            acceleration_mag, acceleration_z = map(float, line.split(','))
            data_list.append((acceleration_mag, acceleration_z))
            ys.append(acceleration_mag)
            if len(data_list) >= window_size:
                prediction = predict_from_buffer(data_list, model)
                print(time.time()-start_time)
                start_time = time.time()
                predictions.append(prediction)
                color = get_color(prediction)
                colors.append(color)
                data_list = data_list[1:]  # Slide window
            animate()

finally:
    s.close()
    plt.ioff()
    plt.show()