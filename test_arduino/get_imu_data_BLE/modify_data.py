import pandas as pd

NUMBER = '1.00'

# Read the .csv file
file_path = f"raw/{NUMBER}_raw.csv" 
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

# Save the modified data into a new .csv file
new_file_path = f"processed/{NUMBER}_processed.csv" 
data.to_csv(new_file_path, index=False)