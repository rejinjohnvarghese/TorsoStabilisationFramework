import pandas as pd 
import matplotlib.pyplot as plt

def plot_ground_truth_labels(file_path):
    # Load the data from the specified file
    data_df = pd.read_csv(file_path)
    
    # Extract necessary columns
    timestamps = data_df['timestamp']
    labels = data_df['label']
    acc_magnitudes = data_df['acceleration_magnitude']
    z_acceleration = data_df['acceleration_z']
    
    # Separate points by their ground truth label
    timestamps_no_fall = timestamps[labels == 0]
    acc_magnitudes_no_fall = acc_magnitudes[labels == 0]
    timestamps_pre_fall = timestamps[labels == 1]
    acc_magnitudes_pre_fall = acc_magnitudes[labels == 1]
    timestamps_fall = timestamps[labels == 2]
    acc_magnitudes_fall = acc_magnitudes[labels == 2]

    # Plot
    plt.figure(figsize=(20, 6))
    plt.scatter(timestamps_no_fall, acc_magnitudes_no_fall, color='green', alpha=0.5, label='No Fall')
    plt.scatter(timestamps_pre_fall, acc_magnitudes_pre_fall, color='orange', alpha=0.5, label='Pre Fall')
    plt.scatter(timestamps_fall, acc_magnitudes_fall, color='red', alpha=0.5, label='Fall')
    
    # Plot z-acceleration for reference
    plt.plot(timestamps, z_acceleration, color='black', label='Z-Acceleration', linewidth=1)

    plt.xlabel('Timestamp')
    plt.ylabel('Acceleration Magnitude')
    plt.title(f'Ground Truth Labels and Acceleration Magnitude - {file_path}')
    plt.legend()
    plt.show()

# Adjust your file path as needed
file_path = 'labelled/labelled_8.1.csv'  # Update this to your actual file path

# Call the function with your ground truth data file path
plot_ground_truth_labels(file_path)