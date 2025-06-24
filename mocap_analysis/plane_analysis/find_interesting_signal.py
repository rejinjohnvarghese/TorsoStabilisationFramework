import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the .trc file
def read_data(filepath):

    df = pd.read_csv(filepath, delimiter="\t", skiprows=4, header=None, low_memory=False)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df = df.reset_index(drop=True)

    # Converting the values in the DataFrame to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    time = df.loc[:, 'Time']

    #Wheelchair back
    #x_wheelchair = df.loc[:, ['X4', 'X5', 'X6', 'X7']]
    #y_wheelchair = df.loc[:, ['Y4', 'Y5', 'Y6', 'Y7']]
    #z_wheelchair = df.loc[:, ['Z4', 'Z5', 'Z6', 'Z7']] 

    # Wheelchair seat
    x_wheelchair = df.loc[:, ['X4', 'X5', 'X6', 'X7']]
    y_wheelchair = df.loc[:, ['Y4', 'Y5', 'Y6', 'Y7']]
    z_wheelchair = df.loc[:, ['Z4', 'Z5', 'Z6', 'Z7']] 

    # Clavicle and shoulders - 11, 12, 13, 17
    #x_body = df.loc[:, ['X11', 'X12', 'X13']]
    #y_body = df.loc[:, ['Y11', 'Y12', 'Y13']]
    #z_body = df.loc[:, ['Z11', 'Z12', 'Z13']] 

    # Clavicle and neck - 11, 12, 14, 16
    x_body = df.loc[:, ['X11', 'X12', 'X16']]
    y_body = df.loc[:, ['Y11', 'Y12', 'Y16']]
    z_body = df.loc[:, ['Z11', 'Z12', 'Z16']] 

    # Right arm - 17, 58, 59
    #x_body = df.loc[:, ['X58', 'X59', 'X17']]
    #y_body = df.loc[:, ['Y58', 'Y59', 'Y17']]
    #z_body = df.loc[:, ['Z58', 'Z59', 'Z17']] 

    # Left arm - 13, 52, 53
    #x_body = df.loc[:, ['X52', 'X53', 'X13']]
    #y_body = df.loc[:, ['Y52', 'Y53', 'Y13']]
    #z_body = df.loc[:, ['Z52', 'Z53', 'Z13']] 

    # Right forearm - 58, 59, 60, 61
    #x_body = df.loc[:, ['X59', 'X60', 'X61']]
    #y_body = df.loc[:, ['Y59', 'Y60', 'Y61']]
    #z_body = df.loc[:, ['Z59', 'Z60', 'Z61']] 

    # Left forearm - 52, 53, 54, 55
    #x_body = df.loc[:, ['X53', 'X54', 'X55']]
    #y_body = df.loc[:, ['Y53', 'Y54', 'Y55']]
    #z_body = df.loc[:, ['Z53', 'Z54', 'Z55']] 

    return time, x_wheelchair, y_wheelchair, z_wheelchair, x_body, y_body, z_body

def angle_between_planes(plane1_points, plane2_points):
    
    # Function to calculate normal vector of a plane
    def normal_vector(points):
        p1, p2, p3 = points
        v1 = np.subtract(p2, p1)
        v2 = np.subtract(p3, p1)
        return np.cross(v1, v2)
    
    n1 = normal_vector(plane1_points)
    n2 = normal_vector(plane2_points)
    
    cos_theta = np.dot(n1, n2) / (np.linalg.norm(n1) * np.linalg.norm(n2))
    angle = np.arccos(np.clip(cos_theta, -1, 1))  # Clipping to handle possible numerical errors
    
    return np.degrees(angle)

def compare_planes_measures(x_wheelchair1, y_wheelchair1, z_wheelchair1, x_body1, y_body1, z_body1, num_rows1, time1, x_wheelchair2, y_wheelchair2, z_wheelchair2, x_body2, y_body2, z_body2, num_rows2, time2, plot_type='angle', which_planes = 'Which planes?'):
    plt.figure(figsize=(10, 6))
    
    def plot_angular_velocity(time, angles):
        return np.gradient(angles, time)
    
    def plot_angular_acceleration(time, speeds):
        return np.gradient(speeds, time)

    angles1 = []  # Store angles for each time point
    angles2 = []  # Store angles for each time point
    
    for i in range(0, num_rows1):
        plane1_points = [(x_wheelchair1.iloc[i, j], y_wheelchair1.iloc[i, j], z_wheelchair1.iloc[i, j]) for j in range(0,3)]
        plane2_points = [(x_body1.iloc[i, j], y_body1.iloc[i, j], z_body1.iloc[i, j]) for j in range(0,3)]    

        angle = angle_between_planes(plane1_points, plane2_points)
        angles1.append(angle)
    
    for i in range(0, num_rows2):
        plane1_points = [(x_wheelchair2.iloc[i, j], y_wheelchair2.iloc[i, j], z_wheelchair2.iloc[i, j]) for j in range(0,3)]
        plane2_points = [(x_body2.iloc[i, j], y_body2.iloc[i, j], z_body2.iloc[i, j]) for j in range(0,3)]
        
        
        angle = angle_between_planes(plane1_points, plane2_points)
        angles2.append(angle)
    
    if plot_type == 'speed':
        values1 = plot_angular_velocity(time1, angles1)
        values2 = plot_angular_velocity(time2, angles2)
        plt.ylabel('Angular Velocity [degrees/s]')
        plt.title('Angular velocity between planes over time - ' + which_planes)
    
    elif plot_type == 'acceleration':
        speeds1 = plot_angular_velocity(time1, angles1)
        values1 = plot_angular_acceleration(time1, speeds1)
        #speeds2 = plot_angular_velocity(time2, angles2)
        #values2 = plot_angular_acceleration(time2, speeds2)
        plt.ylabel('Angular acceleration [$°/s^2$]', fontsize=30)
        plt.title('Angular acceleration between planes over time', fontsize=35)# - ' + which_planes, fontsize=30, pad=20)
    
    else:  # Default is angle
        values1 = angles1
        values2 = angles2
        plt.ylabel('Angles [degrees]')
        plt.title('Angle between planes over time - ' + which_planes)
    
    plt.plot(time1, values1, color='black', label="Fall", linewidth=3)
    #plt.plot(time2, values2, color='b', label = "No fall")
    
    # Printing the max and min values
    # print(f"Max value (Fall/No fall): {max(values1)}/{max(values2)} - Min value: {min(values1)}/{min(values2)}")

    # Calculate min and max values
    max_value1, min_value1 = max(values1), min(values1)
    #max_value2, min_value2 = max(values2), min(values2)

    # Find the corresponding time values for max and min values
    max_time1 = time1[np.argmax(values1)]
    min_time1 = time1[np.argmin(values1)]
    #max_time2 = time2[np.argmax(values2)]
    #min_time2 = time2[np.argmin(values2)]

    # Display max and min values as text on the graph
    #fontsize = 18
    #plt.text(max_time1, max_value1, f"Max: {int(max_value1)}", verticalalignment='bottom', horizontalalignment='center', color='r', fontsize = fontsize)
    #plt.text(min_time1, min_value1, f"Min: {int(min_value1)}", verticalalignment='top', horizontalalignment='center', color='r', fontsize = fontsize)
    #plt.text(max_time2, max_value2, f"Max: {int(max_value2)}", verticalalignment='bottom', horizontalalignment='center', color='b', fontsize = fontsize)
    #plt.text(min_time2, min_value2, f"Min: {int(min_value2)}", verticalalignment='top', horizontalalignment='center', color='b', fontsize = fontsize)

    
    plt.xlabel('Time [s]', fontsize=30)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=fontsize)  # Positioning the legend outside the plot
    plt.grid(True)
    #plt.tight_layout()
    #plt.legend(fontsize=fontsize)
    plt.tick_params(axis='x', labelsize='30') 
    plt.tick_params(axis='y', labelsize='30') 
    plt.show()

file_path1 = '../data/Limit01.trc'
file_path2 = '../data/Forward02.trc'

time1, x_wheelchair1, y_wheelchair1, z_wheelchair1, x_body1, y_body1, z_body1 = read_data(file_path1)
time2, x_wheelchair2, y_wheelchair2, z_wheelchair2, x_body2, y_body2, z_body2 = read_data(file_path2)

num_rows1 = x_wheelchair1.shape[0]
num_rows2 = x_wheelchair2.shape[0]

#plot_plane_angles(x_wheelchair, y_wheelchair, z_wheelchair, x_body, y_body, z_body, num_rows, time, which_planes='Wheelchair seat and clavicle-shoulders')
#plot_plane_angles(x_wheelchair, y_wheelchair, z_wheelchair, x_body, y_body, z_body, num_rows, time, plot_type='speed', which_planes='Wheelchair seat and clavicle-shoulders')
#plot_plane_angles(x_wheelchair, y_wheelchair, z_wheelchair, x_body, y_body, z_body, num_rows, time, plot_type='acceleration', which_planes='Wheelchair seat and clavicle-shoulders')

#compare_planes_measures(x_wheelchair1, y_wheelchair1, z_wheelchair1, x_body1, y_body1, z_body1, num_rows1, time1, x_wheelchair2, y_wheelchair2, z_wheelchair2, x_body2, y_body2, z_body2, num_rows2, time2, which_planes='Wheelchair seat and left forearm')
#compare_planes_measures(x_wheelchair1, y_wheelchair1, z_wheelchair1, x_body1, y_body1, z_body1, num_rows1, time1, x_wheelchair2, y_wheelchair2, z_wheelchair2, #x_body2, y_body2, z_body2, num_rows2, time2, plot_type='speed', which_planes='Wheelchair seat and left forearm')
compare_planes_measures(x_wheelchair1, y_wheelchair1, z_wheelchair1, x_body1, y_body1, z_body1, num_rows1, time1, x_wheelchair2, y_wheelchair2, z_wheelchair2, x_body2, y_body2, z_body2, num_rows2, time2, plot_type='acceleration', which_planes='Wheelchair seat and clavicle-neck')