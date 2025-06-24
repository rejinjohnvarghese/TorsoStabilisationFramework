import pandas as pd
import matplotlib.pyplot as plt

NUMBER = '3.11'

def plot_acceleration(data, measure):
    plt.figure(figsize=(10, 5))
    
    if measure == 'acc_mag': 
        plt.plot(data['timestamp']/1000, data['acceleration_magnitude'])
        plt.title('Acceleration Magnitude over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Acceleration Magnitude [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_mag.png" 
    
    elif measure == 'acc_x':
        plt.plot(data['timestamp']/1000, data['acceleration_x'])
        plt.title('X-Acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('X-Acceleration [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_x.png" 

    elif measure == 'acc_y':
        plt.plot(data['timestamp']/1000, data['acceleration_y'])
        plt.title('Y-Acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Y-Acceleration [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_y.png" 

    elif measure == 'acc_z':
        plt.plot(data['timestamp']/1000, data['acceleration_z'])
        plt.title('Z-Acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Z-Acceleration [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_z.png" 

    elif measure == 'gyro_mag': 
        plt.plot(data['timestamp']/1000, data['gyro_magnitude'])
        plt.title('Gyro Magnitude over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Acceleration Magnitude [rad/s]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_gyro_mag.png" 
    
    elif measure == 'gyro_x':
        plt.plot(data['timestamp']/1000, data['gyro_x'])
        plt.title('X-Gyro over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('X-Gyro [rad/s]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_gyro_x.png" 

    elif measure == 'gyro_y':
        plt.plot(data['timestamp']/1000, data['gyro_y'])
        plt.title('Y-Gyro over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Y-Gyro [rad/s]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_gyro_y.png" 

    elif measure == 'gyro_z':
        plt.plot(data['timestamp']/1000, data['gyro_z'])
        plt.title('Z-Gyro over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Z-Gyro [rad/s]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_gyro_z.png" 
    plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
file_path = f"processed/{NUMBER}_processed_full.csv"  
data = pd.read_csv(file_path)

# Plot the acceleration magnitude over timestamps
plot_acceleration(data, 'acc_mag')
plot_acceleration(data, 'acc_x')
plot_acceleration(data, 'acc_y')
plot_acceleration(data, 'acc_z')
#plot_acceleration(data, 'gyro_mag')
plot_acceleration(data, 'gyro_x')
plot_acceleration(data, 'gyro_y')
plot_acceleration(data, 'gyro_z')

#plt.show()