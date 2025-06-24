import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

NUMBER = '1.10'

def plot(data, measure, threshold):
    plt.figure(figsize=(10, 5))
    time = data['timestamp'] / 1000

    if measure is 'jerk':
        jerk = data[measure]
        above_threshold = jerk >= threshold
        below_threshold = jerk < threshold
        
        plt.plot(time[above_threshold], jerk[above_threshold], color='blue')
        plt.plot(time, data['acceleration_magnitude'], color='black')
        plt.plot(time, data['acceleration_z'], color='green')
        plt.scatter(time[below_threshold], jerk[below_threshold], color='red', s=10)

        plt.title(f'{measure.capitalize().replace("_", " ")} over Time')
        plt.xlabel('Time [s]')
        plt.ylabel(f'{measure.capitalize().replace("acc", "Jerk")} [m/s³]')

    plt.grid(True)
    file_path = f"graphs/{NUMBER}_{measure}.png" 
    #plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
file_path = f"data_with_jerk/{NUMBER}.csv"  
data = pd.read_csv(file_path)
#data = data[:5288]

threshold_value = -25  # Adjust this value as per your requirement

# Plot the acceleration magnitude over timestamps with threshold
plot(data, 'jerk', threshold_value)
# Uncomment the below lines for other measurements
#plot(data, 'acceleration_x', threshold_value)
#plot_acceleration(data, 'acceleration_y', threshold_value)
#plot_acceleration(data, 'acceleration_z', threshold_value)
# plot_acceleration(data, 'gyro_mag', threshold_value)
# plot_acceleration(data, 'gyro_x', threshold_value)
# plot_acceleration(data, 'gyro_y', threshold_value)
# plot_acceleration(data, 'gyro_z', threshold_value)

plt.show()