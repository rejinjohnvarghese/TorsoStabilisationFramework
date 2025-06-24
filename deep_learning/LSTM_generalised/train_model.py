from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.metrics import Recall, Precision
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf 

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.experimental.set_visible_devices(physical_devices[0], 'GPU')

# Load normalized data
data_path1 = "normalized/normalized_8.csv"  # Adjust this path accordingly
data1 = pd.read_csv(data_path1)
data_path2 = "normalized/normalized_11.csv"  # Adjust this path accordingly
data2 = pd.read_csv(data_path2)
data_path4 = "normalized/normalized_3.csv"  # Adjust this path accordingly
data4 = pd.read_csv(data_path4)

data = pd.concat([data1,data2,data4])
#data = data.iloc[::4, :]

# Window size
window_size = 100  # Adjust based on your analysis

# Define the EarlyStopping callback
early_stopping_callback = EarlyStopping(
    monitor='val_accuracy',  # Monitor the validation loss
    patience=20,  # Number of epochs with no improvement after which training will be stopped
    restore_best_weights=True,  # Restore model weights from the epoch with the best value of the monitored metric
    verbose=1  # Print a message when stopping
)

# Define the checkpoint callback
checkpoint_filepath = 'model_checkpoint.h5'  # Specify the filename for the checkpoint
checkpoint_callback = ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=False,  # Set to True if you just want to save the weights, False to save the full model
    monitor='val_accuracy',  # Monitor the validation loss to determine when to save
    mode='max',  # Save the model when the monitored metric decreases ('min' for loss)
    save_best_only=True,  # Set to True if you only want to save when the metric improves
    save_freq='epoch',  # Save after each epoch
    period=10,  # Save every 10 epochs
    verbose=1  # Print a message each time the model is saved
)

def create_sequences(data, window_size):
    X = []
    y = []
    for i in range(len(data) - window_size):
        print(i)
        acc_mag = data['acceleration_magnitude_standardized'][i:i+window_size].values
        z_acc = data['acceleration_z_standardized'][i:i+window_size].values
        sequence = np.stack((acc_mag, z_acc), axis=-1)
        X.append(sequence)
        # Ensure the label index is within the dataframe's range
        if i + window_size < len(data):
            label = data['label'].iloc[i + window_size]  # Use iloc for positional indexing
            y.append(label)
    return np.array(X), np.array(y)

# Create sequences
X, y = create_sequences(data, window_size)

# First Split: Split the data into training (65%) and temp (35%)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.35, random_state=42, stratify=y)

# Calculate the size for validation set from the temp dataset to make it 20% of the total dataset
# Since the temp dataset is 35% of the total, the validation set should be ~57.14% of the temp dataset (20% / 35%)
validation_size = 0.20 / 0.35

# Second Split: Split the temp data into validation (57.14% of temp) and test sets
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=1-validation_size, random_state=42, stratify=y_temp)

# Define the model
model = Sequential()
features = 2

# Add an LSTM layer
model.add(LSTM(units=32, return_sequences=False, input_shape=(window_size, features)))

# Add a Dense layer for classification
model.add(Dense(units=3, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', Recall(), Precision()])

# Model summary
model.summary()

# Convert labels to one-hot encoding
y_train_one_hot = to_categorical(y_train, num_classes=3)
y_val_one_hot = to_categorical(y_val, num_classes=3)
y_test_one_hot = to_categorical(y_test, num_classes=3)

# Modify the model training to use the validation data explicitly
history = model.fit(X_train, y_train_one_hot, epochs=200, batch_size=64, validation_data=(X_val, y_val_one_hot), callbacks=[checkpoint_callback, early_stopping_callback])

# Evaluate the model
test_loss, test_acc, sensitivity, precision = model.evaluate(X_test, y_test_one_hot)
print(f"Test Accuracy: {test_acc*100:.2f}%")
print(f"Test Sensivity: {sensitivity*100:.2f}%")

# Plotting code remains the same
# Plot training and validation loss
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training and Validation Loss Over Epochs')
plt.show()

# Plot training and validation accuracy
plt.figure(figsize=(10, 6))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy Over Epochs')
plt.show()

# Plot training and validation accuracy
plt.figure(figsize=(10, 6))
plt.plot(history.history['recall'], label='Training Recall')
plt.plot(history.history['val_recall'], label='Validation Recall')
plt.xlabel('Epoch')
plt.ylabel('Recall')
plt.legend()
plt.title('Training and Validation Recall Over Epochs')
plt.show()

model.save('model_generalized_200ep_32units.h5')  # Saves the model
# Convert the history.history dict to a pandas DataFrame:     
hist_df = pd.DataFrame(history.history)

filename = 'model_generalized__200ep_32units.csv'

# Save to CSV:
hist_df.to_csv(filename, index=False)
