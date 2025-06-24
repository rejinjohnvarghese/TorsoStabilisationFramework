import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf 

#tf.config.experimental.set_visible_devices([], 'GPU')

data_path = "normalized/normalized_1.4.csv"  # Adjust this path to your data file
data = pd.read_csv(data_path)

# Model loading
#model = load_model('model_combined_0_1_200ep_64units_50Hz.h5')  # Ensure the model name matches
model = load_model('model_1_0_1_2.h5')

window_size = 100  # Window size, ensure consistency with the training phase
predicted_labels = []
timestamps = []  # Collecting timestamps

# Normalize function (assuming global mean and std for each feature are known)
def normalize_data(value, mean, std):
    return (value - mean) / std

# Normalization parameters
acc_mag_mean = 9.958831727261767
acc_mag_std = 0.6981325300451422
acc_z_mean = 7.875712086220169
acc_z_std = 3.210137793501823

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Iterate through data with an overlapping window
for i in range(len(data) - window_size + 1):
    window = data.iloc[i:i+window_size]
    normalized_mag = normalize_data(window['acceleration_magnitude'], acc_mag_mean, acc_mag_std).values
    normalized_z = normalize_data(window['acceleration_z'], acc_z_mean, acc_z_std).values
    
    # Reshape for model input
    model_input = np.stack((normalized_mag, normalized_z), axis=-1).reshape(1, window_size, 2)
    
    # Predict and store the prediction for the last data point of each window
    prediction = model.predict(model_input, verbose=1)
    predicted_label = np.argmax(prediction, axis=1)[0]
    
    # Associate prediction with the last timestamp in the window
    timestamp = window.iloc[-1, window.columns.get_loc('timestamp')]
    timestamps.append(timestamp)
    predicted_labels.append(predicted_label)

# Create a DataFrame to hold the timestamps and predicted labels
results_df = pd.DataFrame({
    'timestamp': timestamps,
    'predicted_label': predicted_labels
})

# Specify the file path to save the predictions
#results_file_path = 'predictions/4.60_combined_200ep_64units_50Hz.csv'
results_file_path = 'pred_1_4_from_1_0_1_2.csv'
results_df.to_csv(results_file_path, index=False)
print(f"Saved predicted labels to {results_file_path}")
