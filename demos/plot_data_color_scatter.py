import pandas as pd
import matplotlib.pyplot as plt

NUMBER = 'C.00'

def plot(data, measure):
    plt.figure(figsize=(10, 5))
    
    # Ensure the data is sorted by timestamp to connect lines correctly
    data_sorted = data.sort_values('timestamp')
    
    # Split data based on solenoid_status
    data_red = data_sorted[data_sorted['solenoid_status'] == 1]
    data_black = data_sorted[data_sorted['solenoid_status'] == 0]
    
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
        # Scatter plot for black points
        plt.scatter(data_black['timestamp']/1000, data_black[measure], c='black', label='Solenoid retracted', s=20)
        # Scatter plot for red points
        plt.scatter(data_red['timestamp']/1000, data_red[measure], c='red', label='Solenoid extended', s=20)
        
        # Connecting lines for visual consistency
        plt.plot(data_sorted['timestamp']/1000, data_sorted[measure], color='gray', linestyle='-', linewidth=2, alpha=0.5)
        
        plt.title(f'{measure.replace("_", " ").title()} over Time', fontsize=35)
        plt.xlabel('Time [s]', fontsize=35, labelpad=5)
        plt.ylabel(y_label_map[measure], fontsize=35, labelpad=10)
        plt.tick_params(axis='x', labelsize='35') 
        plt.tick_params(axis='y', labelsize='35') 
    
    plt.grid(True)
    plt.legend(fontsize=35, markerscale=3)
    # If you need to save the figure, uncomment the next line and provide a path
    # plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
file_path = f"{NUMBER}_processed.csv"  
data = pd.read_csv(file_path)

# Example plot call
plot(data, 'acceleration_magnitude')
plt.show()