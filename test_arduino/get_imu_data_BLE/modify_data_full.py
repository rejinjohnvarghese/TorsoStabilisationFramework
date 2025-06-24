import pandas as pd

NUMBER = '0.01'

# Read the .csv file
file_path = f"raw/{NUMBER}_raw_full.csv" 
data = pd.read_csv(file_path)

# Remove the first line
data = data.drop(index=0) 

# Modify the timestamps
first_timestamp = data['timestamp'].iloc[0]
data['timestamp'] = data['timestamp'] - first_timestamp

# Calculate the magnitude of the acceleration
data['acceleration_magnitude'] = (data['acceleration_x']**2 + 
                                 data['acceleration_y']**2 + 
                                 data['acceleration_z']**2)**0.5

# Calculate the magnitude of the velocity
#data['gyro_magnitude'] = (data['gyro_x']**2 + 
#                                 data['gyro_y']**2 + 
#                                 data['gyro_z']**2)**0.5

# Save the modified data into a new .csv file
new_file_path = f"processed/{NUMBER}_processed_full.csv" 
data.to_csv(new_file_path, index=False)