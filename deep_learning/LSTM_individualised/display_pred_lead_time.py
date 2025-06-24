from scipy.signal import find_peaks
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_predicted_labels_with_lead_times(file_path, raw_file_path=None):
    plt.figure(figsize=(20, 7))
    results_df = pd.read_csv(file_path)
    
    raw_df = pd.DataFrame()
    
    if raw_file_path:
        raw_df = pd.read_csv(raw_file_path)
        z_acceleration = raw_df['acceleration_z'][99:].reset_index(drop=True)
        acc_magnitudes = raw_df['acceleration_magnitude'][99:].reset_index(drop=True)
        results_df = results_df[:len(acc_magnitudes)].reset_index(drop=True)

    timestamps = results_df['timestamp']/1000
    predicted_labels = results_df['predicted_label']
    
    if not raw_df.empty:
        inverted_acc_magnitudes = -acc_magnitudes
        minimal_peaks, _ = find_peaks(inverted_acc_magnitudes, height=-6.5)
    
        start_of_pre_falls = []
        lead_times = []

        for i in range(1, len(predicted_labels)):
            if predicted_labels[i] == 1 and predicted_labels[i-1] == 0:
                start_of_pre_falls.append(i)

        for start_index in start_of_pre_falls:
            subsequent_minimal_peaks = minimal_peaks[minimal_peaks > start_index]
            if len(subsequent_minimal_peaks) > 0:
                next_minimal_peak_index = subsequent_minimal_peaks[0]
                lead_time = (timestamps[next_minimal_peak_index] - timestamps[start_index]) * 1000  # Convert to milliseconds
                if lead_time < 700:  # Check if lead time is less than 500ms
                    lead_times.append(lead_time)
                    plt.plot([timestamps[start_index], timestamps[next_minimal_peak_index]], 
                             [acc_magnitudes[start_index], acc_magnitudes[next_minimal_peak_index]], 'b-')
                    # Annotate with lead time
                    #plt.annotate(f'{lead_time:.2f}ms', 
                    #             (timestamps[start_index], acc_magnitudes[start_index]), 
                    #             textcoords="offset points", xytext=(-30,30), ha='center', color='blue', fontsize=12)

    plt.scatter(timestamps[predicted_labels == 0], acc_magnitudes[predicted_labels == 0], color='green', alpha=0.5, label='No Fall')
    plt.scatter(timestamps[predicted_labels == 1], acc_magnitudes[predicted_labels == 1], color='orange', alpha=0.5, label='Pre Fall')
    plt.scatter(timestamps[predicted_labels == 2], acc_magnitudes[predicted_labels == 2], color='red', alpha=0.5, label='Fall')

    if not raw_df.empty:
        plt.plot(timestamps[:len(z_acceleration)], z_acceleration, color='black', label='Z-Acceleration')

    plt.xlabel('Time [s]', fontsize=30)
    plt.ylabel('Acceleration [m/s²]', fontsize=30)
    plt.tick_params(axis='x', labelsize='30') 
    plt.tick_params(axis='y', labelsize='30') 
    plt.title('Predicted Labels with Lead Times', fontsize=35)
    plt.legend(fontsize=30, markerscale=3, labelspacing=0.2, handletextpad=0.2)
    plt.grid(True)
    plt.show()

# Adjust your file paths as needed
file_path = 'predictions/pred_9.2_from_9.1_9.3.csv'
raw_file_path = 'labelled/labelled_9.2.csv'
plot_predicted_labels_with_lead_times(file_path, raw_file_path)
