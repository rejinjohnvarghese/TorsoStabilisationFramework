import pandas as pd 
import matplotlib.pyplot as plt

def plot_predicted_labels(file_path, raw_file_path=None):
    # Load the predicted labels and associated data from the specified file
    results_df = pd.read_csv(file_path)
    if raw_file_path:
        raw_df = pd.read_csv(raw_file_path)
        #raw_df = raw_df.iloc[::4, :]  # Downsample the data to 50Hz by taking every 4th sample

    # Assume we need to adjust predicted_labels to match acc_magnitudes length
    timestamps = results_df['timestamp']
    predicted_labels = results_df['predicted_label']
    if raw_file_path:
        z_acceleration = raw_df['acceleration_z'][99:].reset_index(drop=True)  # Reset index after slicing
        acc_magnitudes = raw_df['acceleration_magnitude'][99:].reset_index(drop=True)  # Reset index after slicing
        # Ensure predicted_labels is aligned in length and index with acc_magnitudes
        predicted_labels = predicted_labels[:len(acc_magnitudes)].reset_index(drop=True)  # Adjust length and reset index

    # Now proceed with your original logic, indices should align now
    timestamps_no_fall = timestamps[predicted_labels == 0]
    acc_magnitudes_no_fall = acc_magnitudes[predicted_labels == 0]
    timestamps_pre_fall = timestamps[predicted_labels == 1]
    acc_magnitudes_pre_fall = acc_magnitudes[predicted_labels == 1]
    timestamps_fall = timestamps[predicted_labels == 2]
    acc_magnitudes_fall = acc_magnitudes[predicted_labels == 2]

    # Plot
    plt.figure(figsize=(20, 6))
    plt.scatter(timestamps_no_fall, acc_magnitudes_no_fall, color='green', alpha=0.5, label='No Fall')
    plt.scatter(timestamps_pre_fall, acc_magnitudes_pre_fall, color='orange', alpha=0.5, label='Pre Fall')
    plt.scatter(timestamps_fall, acc_magnitudes_fall, color='red', alpha=0.5, label='Fall')

    # Add z-acceleration plot if available
    if raw_file_path:
        plt.plot(timestamps[:len(z_acceleration)], z_acceleration, color='black', label='Z-Acceleration')  # Adjust timestamp to match z_acceleration length

    plt.xlabel('Timestamp')
    plt.ylabel('Acceleration Magnitude')
    plt.title(f'Acceleration Magnitude and Predicted Labels for Each Data Point - {file_path}')
    plt.legend()
    
# Adjust your file paths as needed
#file_paths = ['predictions/4.60_combined_200ep_4units.csv']
file_paths = ['predictions/pred_1.4_from_1.1_1.3.csv']
              #'pred_1_4_from_1_0_1_2.csv']
raw_file_paths = ['labelled/labelled_1.4.csv']
                  #'labelled/labelled_1.4.csv']

for file_path, raw_file_path in zip(file_paths, raw_file_paths):
    plot_predicted_labels(file_path, raw_file_path)

plt.show()
