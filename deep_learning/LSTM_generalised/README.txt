This folder contains training dataset, training code, test code, models and plot code for the generalised LSTM neural networks 

labelled 
experiment trials with each datapoint labelled as either 0, 1 or 2 corresponding respectively to non-fall, pre-fall and fall classes 
name format is labelled_X.Y, where X correspond to the subject and Y to the trial. There are 5 trials by subject normally. X=0 are tests on me.

normalised 
experiment trials normalised using mean and standard deviation across all subjects and trials
the 5 experiment trials of a specific subject are combined into one .csv file saved as normalized_X.csv with X corresponding to the subject 

predictions
contain the predictions (tests) for the final generalised model 
saved in the following format: pred_X.W_from_generalised.csv, with X the subject number, W the trial used for testing

model_generalised_200ep_32units.h5
final generalised model, trained with 200ep, batch size 64, LSTM layer of 32 units
further investigation might be necessary to train a better model (bigger dataset, other signals, other architecture)

predictions
contain the predictions (tests) for the individualised models 
saved in the following format: pred_X.W_from_generalized.csv, with X the subject number and W the trial used for testing 

display_pred_lead_time.py 
python code to display the predictions for a specific trial with the corresponding lead time 
used to verify visually capabilities of the neural network and to generate graphs for the report/presentation 

display_predictions.py 
python code to display the predictions for a specific trial 

IMU_simulator.py 
python code to simulate how an IMU would sent the data to the model for real-time prediction (use in combination with real_time_scatter.py)
too slow to be used, might exist a better way to do it 
future step: deploy the neural network on a microcontroller 

real_time_scatter.py 
python code to receive the data from IMU_simulator.py 
too slow to be used, might exist a better way to do it 
future step: deploy the neural network on a microcontroller 

show_ground_truth.py 
python code to display the labels of an experiment trial (ground truth, not prediction by the model)

test_model.py
python code to test an individualised model
predict the labels of the selected trials and save in a .csv file 

test_model_faster.py 
faster version of test_model.py 

test_multiple.py
python code to output the prediction for multiple test files 
taken from the individualised version, for which we need to specify the training and testing files (to find the right model), so not optimised for generalised version 

train_model.py
python code to train an individualised model from two experiments trials 





