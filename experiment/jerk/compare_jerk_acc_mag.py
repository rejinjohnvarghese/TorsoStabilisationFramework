import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

NUMBER = '1.10'

numbers = ['0.12', '0.20', '0.30', '0.40', '0.50', '0.60', '0.70', '0.80', '1.10', '1.20', '2.10', '3.00', '4.00', '5.00', '6.00']

def plot(data, threshold_jerk, threshold_acc_mag):
    fig, ax = plt.subplots(3, 1, figsize=(10, 5), sharex=True)
    time = data['timestamp'] / 1000
   

    # Jerk plot
    jerk = data['jerk']
    above_threshold = jerk >= threshold_jerk
    below_threshold = jerk < threshold_jerk
    ax[0].plot(time[above_threshold], jerk[above_threshold], color='blue')
    ax[0].scatter(time[below_threshold], jerk[below_threshold], color='red', s=10)
    ax[0].set_xlabel('Time [s]')
    ax[0].set_ylabel(f'Jerk [m/s³]')
    ax[0].grid(True)

    # Acc Mag plot
    acc_mag = data['acceleration_magnitude']
    above_threshold = acc_mag >= threshold_acc_mag
    below_threshold = acc_mag < threshold_acc_mag
    ax[1].plot(time[above_threshold], acc_mag[above_threshold], color='blue')
    ax[1].scatter(time[below_threshold], acc_mag[below_threshold], color='red', s=10)
    ax[1].set_xlabel('Time [s]')
    ax[1].set_ylabel(f'Acc Mag [m/s²]')
    ax[1].grid(True)

    # Acceleration z plot
    ax[2].plot(time, data['acceleration_z'], color='black')
    ax[2].set_xlabel('Time [s]')
    ax[2].set_ylabel(f'Z Acc [m/s²]')
    ax[2].grid(True)
# Read the .csv file
file_path = f"data_with_jerk/{NUMBER}.csv"  
data = pd.read_csv(file_path)
#data = data[:5288]

threshold_jerk = -20  # Adjust this value as per your requirement
threshold_acc_mag = 8.4

# Plot the acceleration magnitude over timestamps with threshold
plot(data, threshold_jerk, threshold_acc_mag)
# Uncomment the below lines for other measurements
#plot(data, 'acceleration_x', threshold_value)
#plot_acceleration(data, 'acceleration_y', threshold_value)
#plot_acceleration(data, 'acceleration_z', threshold_value)
# plot_acceleration(data, 'gyro_mag', threshold_value)
# plot_acceleration(data, 'gyro_x', threshold_value)
# plot_acceleration(data, 'gyro_y', threshold_value)
# plot_acceleration(data, 'gyro_z', threshold_value)

plt.show()