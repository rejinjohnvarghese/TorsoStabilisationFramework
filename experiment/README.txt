This folder contains data and code from the experiment, as well as analysis for the threshold-based fall detection strategies

get_data
data and code from/for the experiment 

get_data/raw
raw data from the experiment
name format is X.Y0, where X correspond to the subject and Y to the trial. There are 5 trials by subject normally. X=0 are tests on me.
data consists of acceleration, gyroscope and magnetometer values in X,Y,Z with timestamps 

get_data/processed
processed data with an additional column for the acceleration magnitude and timestamps starting at zero 
processed by process.py 

get_data/videos 
videos of some experiments trials 
videos were recorded only for a few trials, not everytime 

get_data/find_threshold.py 
python code to test which threshold could be suitable for a subject 

get_data/lead_time.py
python code to plot the lead time for a specific fall of a trial
used on a few trial to get an estimation of the lead time 

get_data/plot.py 
python code to plot different measurements of the experiment 
mainly used right after a trial to verify is everything went as expected 

get_data/process.py 
python code to modify the raw data: make the timestamps start at zero and add an additional column for the acceleration_magnitude 

get_data/save_data.py
python code to receive data from the MCU during an experiment trial as well as taking a video in the same time 


jerk 
attempt to use the jerk instead/in combination with the acceleration magnitude for threshold-based fall detection 

jerk/data_with_jerk
processed data with an additional column for the jerk 
not all the trials were used because the jerk proved rapidly to be complicated to use for threshold-based approach 

jerk/add_jerk_data.py
python code to add the jerk to the data 

jerk/compare_jerk_acc_mag.py
python code to plot and compare the acceleration magnitude and the jerk 

jerk/find_threshold.py 
python code to find the jerk threshol for a specific subject 