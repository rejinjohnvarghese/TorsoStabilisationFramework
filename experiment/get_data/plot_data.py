import pandas as pd
import matplotlib.pyplot as plt

NUMBER = '5.50'

def plot(data, measure):
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
    #plt.savefig(file_path)
    #plt.show(block = False)
        
    elif measure == 'roll': 
        plt.plot(data['timestamp'], data['roll'])
        plt.title('Roll over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Roll (deg)')
        plt.grid(True)
        #file_path = f"graphs/{NUMBER}_acc_mag.png" 
    
    elif measure == 'pitch': 
        plt.plot(data['timestamp'], data['pitch'])
        plt.title('Pitch over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Pitch (deg)')
        plt.grid(True)
        #file_path = f"graphs/{NUMBER}_acc_mag.png" 
    
    elif measure == 'yaw': 
        plt.plot(data['timestamp'], data['yaw'])
        plt.title('Yaw over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Yaw (deg)')
        plt.grid(True)
        #file_path = f"graphs/{NUMBER}_acc_mag.png" 
    
    elif measure == 'vertical_acceleration': 
        plt.plot(data['timestamp'], data['vertical_acceleration'])
        plt.title('Vertical acceleration over Time')
        plt.xlabel('Time [s]')
        plt.ylabel('Vertica acceleration [m/s²]')
        plt.grid(True)
        #file_path = f"graphs/{NUMBER}_acc_mag.png" 


# Read the .csv file
file_path = f"processed/{NUMBER}_processed.csv"  
data = pd.read_csv(file_path)

#file_path_2 = f"ahrs/{NUMBER}_ahrs.csv"  
#data_ahrs = pd.read_csv(file_path_2)

# Plot the acceleration magnitude over timestamps
plot(data, 'acc_mag')
#plot(data, 'acc_x')
#plot(data, 'acc_y')
plot(data, 'acc_z')
#plot(data, 'gyro_mag')
#plot(data, 'gyro_x')
#plot(data, 'gyro_y')
#plot(data, 'gyro_z')
#plot(data, 'roll')
#plot(data, 'pitch')
#plot(data, 'yaw')
#plot(data_ahrs, 'vertical_acceleration')

plt.show()


