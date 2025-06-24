import pandas as pd
import matplotlib.pyplot as plt

NUMBER = '1.00'

def plot_acceleration(data, measure):
    plt.figure(figsize=(10, 5))
    
    if measure == 'mag': 
        plt.plot(data['timestamp']/1000, data['acceleration_magnitude'])
        plt.title('Acceleration Magnitude over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Acceleration Magnitude [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_mag.png" 
    
    elif measure == 'x':
        plt.plot(data['timestamp']/1000, data['acceleration_x'])
        plt.title('X-Acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('X-Acceleration [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_x.png" 

    elif measure == 'y':
        plt.plot(data['timestamp']/1000, data['acceleration_y'])
        plt.title('Y-Acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Y-Acceleration [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_y.png" 

    elif measure == 'z':
        plt.plot(data['timestamp']/1000, data['acceleration_z'])
        plt.title('Z-Acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Z-Acceleration [m/s²]')
        plt.grid(True)
        file_path = f"graphs/{NUMBER}_acc_z.png" 

    plt.savefig(file_path)
    #plt.show(block = False)

# Read the .csv file
file_path = f"processed/{NUMBER}_processed.csv"  
data = pd.read_csv(file_path)

# Plot the acceleration magnitude over timestamps
plot_acceleration(data, 'mag')
plot_acceleration(data, 'x')
plot_acceleration(data, 'y')
plot_acceleration(data, 'z')

plt.show()