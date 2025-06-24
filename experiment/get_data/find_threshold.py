import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

NUMBER = '4.00'

def plot_acceleration(data, measure, threshold):
    plt.figure(figsize=(10, 5))
    time = data['timestamp'] / 1000

    if measure in ['acceleration_magnitude', 'acceleration_x', 'acceleration_y', 'acceleration_z']:
        acceleration = data[measure]
        above_threshold = acceleration >= threshold
        below_threshold = acceleration < threshold
        
        plt.plot(time[above_threshold], acceleration[above_threshold], color='blue')
        plt.scatter(time[below_threshold], acceleration[below_threshold], color='red', s=10)

        plt.title(f'{measure.capitalize().replace("_", " ")} over Time')
        plt.xlabel('Time [s]')
        plt.ylabel(f'{measure.capitalize().replace("acc", "Acceleration")} [m/s²]')

    elif measure in ['gyro_mag', 'gyro_x', 'gyro_y', 'gyro_z']:
        gyro = data[measure]
        above_threshold = gyro >= threshold
        below_threshold = gyro < threshold
        
        plt.plot(time[above_threshold], gyro[above_threshold], color='blue')
        plt.scatter(time[below_threshold], gyro[below_threshold], color='red')

        plt.title(f'{measure.capitalize().replace("_", " ")} over Time')
        plt.xlabel('Time [s]')
        plt.ylabel(f'{measure.capitalize().replace("gyro", "Gyro")} [rad/s]')

    plt.grid(True)
    file_path = f"graphs/{NUMBER}_{measure}.png" 
    #plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
file_path = f"processed/{NUMBER}_processed.csv"  
data = pd.read_csv(file_path)
#data = data[:5288]

threshold_value = 8.6  # Adjust this value as per your requirement

# Plot the acceleration magnitude over timestamps with threshold
plot_acceleration(data, 'acceleration_magnitude', threshold_value)
# Uncomment the below lines for other measurements
#plot_acceleration(data, 'acceleration_x', threshold_value)
#plot_acceleration(data, 'acceleration_y', threshold_value)
#plot_acceleration(data, 'acceleration_z', threshold_value)
# plot_acceleration(data, 'gyro_mag', threshold_value)
# plot_acceleration(data, 'gyro_x', threshold_value)
# plot_acceleration(data, 'gyro_y', threshold_value)
# plot_acceleration(data, 'gyro_z', threshold_value)

plt.show()