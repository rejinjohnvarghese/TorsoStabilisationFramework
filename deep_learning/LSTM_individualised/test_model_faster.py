from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf


# Load the data
data_path = "labelled/labelled_1.3.csv"
data = pd.read_csv(data_path)

# Load the model
model_path = 'model_1.0_1.2.h5'
model = load_model(model_path)

# Normalization parameters
acc_mag_mean = 9.958831727261767
acc_mag_std = 0.6981325300451422
acc_z_mean = 7.875712086220169
acc_z_std = 3.210137793501823

# Normalize the dataset
data['acceleration_magnitude'] = (data['acceleration_magnitude'] - acc_mag_mean) / acc_mag_std
data['acceleration_z'] = (data['acceleration_z'] - acc_z_mean) / acc_z_std

# Window size and batch size
window_size = 100
batch_size = 64

# Function to generate windows in batches
def generate_windows(data, window_size, batch_size):
    num_windows = len(data) - window_size + 1
    for i in range(0, num_windows, batch_size):
        end_index = min(i + batch_size, num_windows)
        windows = np.array([data[['acceleration_magnitude', 'acceleration_z']].iloc[j:j+window_size].values for j in range(i, end_index)])
        yield windows, data['timestamp'].iloc[i+window_size-1:end_index+window_size-1].values

# Predicting in batches
predicted_labels = []
timestamps = []

for windows, batch_timestamps in generate_windows(data, window_size, batch_size):
    # Reshape for model input if necessary
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
results_file_path = 'pred_1.3_from_1.0_1.2.csv'
results_df.to_csv(results_file_path, index=False)
print(f"Saved predicted labels to {results_file_path}")

# Assuming you have a 'true_label' column in your data
true_labels = data['label'].iloc[window_size-1:].values  # Adjust indexing based on window size

# Define a function to calculate sensitivity, specificity, accuracy, and F1-score for each class
def calculate_metrics(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    true_positives = np.diag(cm)
    false_positives = np.sum(cm, axis=0) - true_positives
    false_negatives = np.sum(cm, axis=1) - true_positives
    true_negatives = np.sum(cm) - (true_positives + false_positives + false_negatives)
    
    sensitivity = true_positives / (true_positives + false_negatives)
    specificity = true_negatives / (true_negatives + false_positives)
    accuracy = (true_positives + true_negatives) / np.sum(cm)
    
    precision = true_positives / (true_positives + false_positives)
    recall = sensitivity
    f1 = 2 * (precision * recall) / (precision + recall)
    
    return sensitivity, specificity, accuracy, f1

# Calculate and print metrics
#sensitivity, specificity, accuracy, f1 = calculate_metrics(true_labels, predicted_labels)
#print("Sensitivity:", sensitivity)
#print("Specificity:", specificity)
#print("Accuracy:", accuracy)
#print("F1-Score:", f1)