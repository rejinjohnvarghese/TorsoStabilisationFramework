import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd 

# Read the .trc file
file_path = '../data/Limit01.trc'
#file_path = '../data/Forward02.trc'

df = pd.read_csv(file_path, delimiter="\t", skiprows=4, header=None, low_memory=False)
df.columns = df.iloc[0]
df = df.drop(df.index[0])
df = df.reset_index(drop=True)

# Converting the values in the DataFrame to numeric
df = df.apply(pd.to_numeric, errors='coerce')

# Getting the first row values from columns X1 to X10, Y1 to Y10, and Z1 to Z10
#x = df.loc[1000, ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10']]
#y = df.loc[1000, ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Y10']]
#z = df.loc[1000, ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10']]

x = df.loc[0, 'X1':'X63':3]
y = df.loc[0, 'Y1':'Y63':3]
z = df.loc[0, 'Z1':'Z63':3]

# Creating a new figure for the 3D plot
fig = plt.figure()

# Creating 3D plot
ax = fig.add_subplot(111, projection='3d')

# Adding the points to the plot
ax.scatter(x, y, z)

# Adding labels to the points
for i in range(10):
    ax.text(x[i], y[i], z[i], '%s' % (str(i+1)), size=12, color='red')

# Adding labels to the axes
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Showing the plot
plt.show()