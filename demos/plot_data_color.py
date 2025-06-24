import pandas as pd
import matplotlib.pyplot as plt

NUMBER = 'A.00'

def plot(data, measure):
    plt.figure(figsize=(10, 5))

        
    # Extract timestamps divided by 1000 if necessary
    time_scale_factor = 1000 if measure in ['acc_mag', 'acc_x', 'acc_y', 'acc_z', 'gyro_mag', 'gyro_x', 'gyro_y', 'gyro_z'] else 1
    timestamps = data['timestamp'] / time_scale_factor
    
    # Define color based on solenoid_status
    colors = data['solenoid_status'].map({0: 'black', 1: 'red'})
    
    if measure in ['acceleration_magnitude', 'acc_x', 'acc_y', 'acc_z', 'gyro_mag', 'gyro_x', 'gyro_y', 'gyro_z']:
        y_label_map = {
            'acceleration_magnitude': 'Acceleration Magnitude [m/s²]',
            'acc_x': 'X-Acceleration [m/s²]',
            'acc_y': 'Y-Acceleration [m/s²]',
            'acc_z': 'Z-Acceleration [m/s²]',
            'gyro_mag': 'Gyro Magnitude [rad/s]',
            'gyro_x': 'X-Gyro [rad/s]',
            'gyro_y': 'Y-Gyro [rad/s]',
            'gyro_z': 'Z-Gyro [rad/s]'
        }
    # Plot each segment based on solenoid_status
    for i in range(len(data) - 1):
        # Determine color
        color = 'red' if data.loc[i, 'solenoid_status'] == 1 else 'black'
        
        # Plot segment
        plt.plot(timestamps[i:i+2], data[measure][i:i+2], color=color)
    
    plt.grid(True)
    plt.grid(True)
    plt.legend()
    # If you need to save the figure, uncomment the next line and provide a path
    # plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
file_path = f"{NUMBER}_processed.csv"  
data = pd.read_csv(file_path)

# Example plot call
plot(data, 'acceleration_magnitude')
plt.show()
