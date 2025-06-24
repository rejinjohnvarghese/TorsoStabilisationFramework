import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

NUMBER = '6.00'

# Function to apply a low-pass Butterworth filter
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Read the .csv file
file_path = f"../get_data/processed/{NUMBER}_processed.csv"  
data = pd.read_csv(file_path)

# Filter settings
cutoff_frequency = 5  # Cutoff frequency in Hz (adjust based on your analysis)
sampling_rate = 208  # Sampling rate in Hz
data['filtered_acc_mag'] = butter_lowpass_filter(data['acceleration_magnitude'], cutoff_frequency, sampling_rate)

# Calculate jerk from the filtered acceleration magnitude
time_step = 1 / sampling_rate  # Time step in seconds
data['jerk'] = np.append(np.diff(data['filtered_acc_mag']) / time_step, 0)  # Append 0 for the last value to maintain array size

# Save the DataFrame with the jerk column to a new CSV file
new_file_path = f"data_with_jerk/{NUMBER}.csv"
data.to_csv(new_file_path, index=False)
