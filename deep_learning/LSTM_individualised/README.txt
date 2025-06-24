This folder contains training dataset, training code, test code, models and plot code for the individualised LSTM neural networks 

labelled 
experiment trials with each datapoint labelled as either 0, 1 or 2 corresponding respectively to non-fall, pre-fall and fall classes.
name format is labelled_X.Y, where X correspond to the subject and Y to the trial. There are 5 trials by subject normally. X=0 are tests on me.

normalised 
experiment trials normalised for each subject (using mean and standard deviation of the subject) 
name format is normalized_X.Y, where X correspond to the subject and Y to the trial. There are 5 trials by subject normally. X=0 are tests on me.

models
contain the different individualised models 
saved in the following format: model_X.Y_X.Z.h5, with X the subject number, Y and Z the two trials used for training 

predictions
contain the predictions (tests) for the individualised models 
saved in the following format: pred_X.W_from_X.Y_X.Z.csv, with X the subject number, W the trial used for testing, Y and Z the two trials used for training the model 

compare_lead_time.py 
python code to compare (plot) the lead time for the threshold-based approach and the deep learning approach for a specific trial 
mainly used to generate graph for the report/presentation 

display_pred_lead_time.py 
python code to display the predictions for a specific trial with the corresponding lead time 
used to verify the capabilities of the neural network and to generate graphs for the report/presentation 

display_predictions.py 
python code to display the predictions for a specific trial 

train_model.py
python code to train an individualised model from two experiments trials 

test_model.py
python code to test an individualised model
predict the labels of the selected trials and save in a .csv file 

test_model_faster.py 
faster version of test_model.py 

test_multiple.py
python code to output the prediction for multiple training/test files combination 
need to specifiy the training files to find the right model and the testing files for the predictions 
similar to test_model.py, but run accross all the specified combinations instead of restarting the script every time 



