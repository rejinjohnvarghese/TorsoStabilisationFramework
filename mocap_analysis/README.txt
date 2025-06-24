This folder contains code and data for the MOCAP analysis

data
Contains the data from the MOCAP experiment as .trc files 
They represent the position of each markers in the 3D space with XYZ coordinates
They are read by the different Python codes to analyse the trajectory and detect the pattern 

plane_analysis
Analysis of the angle, angular velocity and angular acceleration between different planes constructed from the MOCAP markers

plane_analysis/find_interesting_signal.py
Python code to plot and compare the angle, angular velocity and angular acceleration between different planes
Used to identify which signal displays a pattern that can be used to identify a fall (distinguish between non-fall and fall movements)

plane_analysis/identify_wheelchair_markers.py 
Python code to identify the position of the markers on the weelchair in order to construct the wheelchair seat plane 

plane_analysis/markersIdentification.png 
Result of the wheelchair markers identification 

4 folders "plane_analysis/Wheelchair_seat_XX"
Contain evolution of the angle, angular velocity and angular acceleration between the wheelchair seat planes and another plane (constructed using the MOCAP markers)
Used to identify where the device should be placed as well as to verify the presence of the fall pattern 

