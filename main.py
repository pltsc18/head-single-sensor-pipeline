# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:17:31 2023

@author: paolo
"""
                                                                               
# import packages
import os
from scipy import io
from tensorflow import keras
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

# get current directory
current_dir = os.getcwd()
# functions directory
fun_dir = os.path.join(current_dir,'utils_','functions_.py')
# run function_.py
runfile(fun_dir, wdir=os.path.join(current_dir,'utils_'))
# import all functions in functions_.py
from functions_ import *

# paths
sub_dir = '0001' # CHANGE WITH DESIRED SUBJECT NAME
model_dir = os.path.join(current_dir,'MyModel6') # Directory containing tensorflow assets of trained model
data_path = os.path.join(current_dir,sub_dir,'data.mat')
save_path = os.path.join(current_dir,sub_dir,'output.mat')

# loading TCN data
f = loadmat(data_path) # load .mat variable
# delete  
if 'model' in globals():
    del model 
model = keras.models.load_model(model_dir,compile= False)
#
dataset = f["pre_processed_data"]

# main loop
print('Processing subject',sub_dir,'...')
for iTest in list(dataset["TimeMeasure1"].keys()): # e.g. 'Test3' 
    for iTrial in list(dataset["TimeMeasure1"][iTest].keys()): # e.g. 'Trial1'
        print('Processing',iTest,iTrial)   
        data = dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"] 
        if type(data) is dict:
            mWB = data
            # processed windows during current mWB
            x = mWB["dataset_p"]
            # reshape dataset
            x, t = buildDataSet(x)
            # evaluation of extra ICs, missed ICs, time errors, predicted ICs and target ICs for each mWB
            ExtraEvents, MissedEvents, Predicted_Initial_Contact_Events, Target_Initial_Contact_Events = modelEvaluate(model,x,t)
            # saving into dict
            dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"]["ExtraEvents"] = ExtraEvents 
            dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"]["MissedEvents"] = MissedEvents 
            dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"]["Predicted_Initial_Contact_Events"] = Predicted_Initial_Contact_Events 
            dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"]["Target_Initial_Contact_Events"] = Target_Initial_Contact_Events 
        else:
            for mWBi in range(len(data)): 
                mWB = data[mWBi]
                # processed windows during current mWB
                x = mWB.dataset_p
                # reshape dataset
                x, t = buildDataSet(x)
                # evaluation of extra ICs, missed ICs, time errors, predicted ICs and target ICs for each mWB
                ExtraEvents, MissedEvents, Predicted_Initial_Contact_Events, Target_Initial_Contact_Events = modelEvaluate(model,x,t)
                # saving into dict
                dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"][mWBi].ExtraEvents = ExtraEvents 
                dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"][mWBi].MissedEvents = MissedEvents 
                dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"][mWBi].Predicted_Initial_Contact_Events = Predicted_Initial_Contact_Events 
                dataset["TimeMeasure1"][iTest][iTrial]["Standards"]["INDIP"]["MicroWB"][mWBi].Target_Initial_Contact_Events = Target_Initial_Contact_Events 
# saving
io.savemat(save_path, dataset, long_field_names = True, oned_as='column')
