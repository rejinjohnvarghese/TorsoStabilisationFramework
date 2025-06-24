import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

NUMBER = '3.00'
FALL_NUMBER = 2

def show_lead_time(data, measure, threshold, peak_threshold):
    plt.figure(figsize=(10, 5))
    time = data['timestamp'] / 1000
    values = data[measure]
    ylabel = f'{measure.capitalize().replace("_", " ")}'

    # Coloring based on threshold
    colors = ['red' if val < threshold else 'blue' for val in values]
    plt.scatter(time, values, color=colors, s=10)

    # Finding the first value below threshold
    below_threshold_indices = np.where(values < threshold)[0]
    if len(below_threshold_indices) > 0:
        first_below_threshold_idx = below_threshold_indices[0]
        time_first_below = time[first_below_threshold_idx]

        # Finding the first peak above peak_threshold after the first below threshold point
        after_fall_indices = np.where(time > time_first_below)[0]
        peak_above_threshold_indices = np.where(values[after_fall_indices] > peak_threshold)[0]
        if len(peak_above_threshold_indices) > 0:
            first_peak_idx = after_fall_indices[peak_above_threshold_indices[0]]
            time_peak = time[first_peak_idx]

            # Drawing a horizontal line and annotating the lead time
            plt.hlines(y=values[first_below_threshold_idx], xmin=time_first_below, xmax=time_peak, color='green', linestyles='dashed')
            plt.vlines(x=time_peak, ymin=values[first_below_threshold_idx], ymax=values[first_peak_idx], color='green', linestyles='dashed')
            lead_time = time_peak - time_first_below
            plt.annotate(f'Lead time: {lead_time:.2f}s', xy=((time_first_below + time_peak) / 2, values[first_below_threshold_idx]), 
                         xytext=(0, 10), textcoords='offset points', ha='center', va='bottom')

    plt.title(f'{ylabel} over Time')
    plt.xlabel('Time [s]')
    plt.ylabel(ylabel)
    plt.grid(True)
    file_path = f"graphs/{NUMBER}_{measure}.png" 
    #plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
#file_path = f"processed/{NUMBER}_fall_{FALL_NUMBER}.csv"  
#data = pd.read_csv(file_path)

threshold_value = 8.3  # Adjust this value as per your requirement
peak_threshold = 22.2
peak_thresholds = [12.3, 12.2]

# Plot the acceleration magnitude over timestamps with threshold
#plot_acceleration(data, 'acceleration_magnitude', threshold_value)
# Uncomment the below lines for other measurements
#plot_acceleration(data, 'acceleration_x', threshold_value)
#plot_acceleration(data, 'acceleration_y', threshold_value)
#plot_acceleration(data, 'acceleration_z', threshold_value)
# plot_acceleration(data, 'gyro_mag', threshold_value)
# plot_acceleration(data, 'gyro_x', threshold_value)
# plot_acceleration(data, 'gyro_y', threshold_value)
# plot_acceleration(data, 'gyro_z', threshold_value)

#show_lead_time(data, 'acceleration_magnitude', threshold_value, peak_threshold)

for i, peaks in enumerate(peak_thresholds):
    FALL_NUMBER = i+1
    file_path = f"processed/{NUMBER}_fall_{FALL_NUMBER}.csv"  
    data = pd.read_csv(file_path)
    show_lead_time(data, 'acceleration_magnitude', threshold_value, peak_thresholds[i])

plt.show()