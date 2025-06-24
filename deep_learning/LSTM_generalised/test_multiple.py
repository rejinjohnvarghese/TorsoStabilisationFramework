from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf

test_comb = [
    ('1.1', '1.3', '1.4'),
    ('1.0', '1.2', '1.4'),
    ('1.1', '1.2', '1.3'),

    ('4.1', '4.3', '4.4'),
    ('4.0', '4.2', '4.4'),
    ('4.1', '4.2', '4.3'),

    ('5.1', '5.3', '5.4'),
    ('5.0', '5.2', '5.4'),
    ('5.1', '5.2', '5.3'),

    ('7.1', '7.3', '7.4'),
    ('7.0', '7.2', '7.4'),
    ('7.1', '7.2', '7.3'),

    ('9.1', '9.3', '9.4'),
    ('9.0', '9.2', '9.4'),
    ('9.1', '9.2', '9.3'),
    # Add more combinations as needed
]

# Normalization parameters
acc_mag_mean = 9.958831727261767
acc_mag_std = 0.6981325300451422
acc_z_mean = 7.875712086220169
acc_z_std = 3.210137793501823

window_size = 100
batch_size = 64

def normalize_data(data):
    data['acceleration_magnitude'] = (data['acceleration_magnitude'] - acc_mag_mean) / acc_mag_std
    data['acceleration_z'] = (data['acceleration_z'] - acc_z_mean) / acc_z_std
    return data

def generate_windows(data, window_size, batch_size):
    num_windows = len(data) - window_size + 1
    for i in range(0, num_windows, batch_size):
        end_index = min(i + batch_size, num_windows)
        windows = np.array([data[['acceleration_magnitude', 'acceleration_z']].iloc[j:j+window_size].values for j in range(i, end_index)])
        yield windows, data['timestamp'].iloc[i+window_size-1:end_index+window_size-1].values

# Assuming models_comb and test_comb are defined as shown previously
for test_files in test_comb:
    model_path = f'model_generalized_200ep_32units.h5'
    model = load_model(model_path)
    
    for test_file in test_files:
        # Load and normalize the test data
        data_path = f"../LSTM_individual/labelled/labelled_{test_file}.csv"
        data = pd.read_csv(data_path)
        data = normalize_data(data)
        
        predicted_labels = []
        timestamps = []
        
        for windows, batch_timestamps in generate_windows(data, window_size, batch_size):
            windows_reshaped = windows.reshape(windows.shape[0], window_size, 2)
            predictions = model.predict(windows_reshaped, verbose=0)
            predicted_labels_batch = np.argmax(predictions, axis=1)
            
            predicted_labels.extend(predicted_labels_batch)
            timestamps.extend(batch_timestamps)
        
        # Create a DataFrame to hold the timestamps and predicted labels
        results_df = pd.DataFrame({
            'timestamp': timestamps,
            'predicted_label': predicted_labels
        })
        
        # Specify the file path to save the predictions
        results_file_path = f'predictions/pred_{test_file}_from_generalized.csv'
        results_df.to_csv(results_file_path, index=False)
        print(f"Saved predicted labels to {results_file_path}")
