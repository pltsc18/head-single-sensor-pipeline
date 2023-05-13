# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:07:06 2023

@author: paolo

Functions for training the TCN models for the detection of the initial contacts
"""
# packages
from scipy import io
import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
from tcn import TCN, tcn_full_summary
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def compare_events(annotated, predicted, thr=50, filename_prefix=None):
    """
    Compares the timings of the annotated (true) events and the predicted events.
    Parameters
    ----------
    annotated : array
        A numpy array with the indexes of annotated gait events.
    predicted : array
        A numpy array with the indexes of predicted gait events.
    thr : int
        Threshold (in samples) that determines which time difference is allowed,
        between the annotated and predicted event for it to be considered a match.
    """

    if len(annotated)==0 and len(predicted)==0:
        # print("No gait events annotated, no gait events detected!")
        return np.array([]), np.array([]), np.array([])
    if len(annotated)!=0 and len(predicted)==0:
        # if filename_prefix is not None:
        #     print(f"{len(annotated)} gait events annotated, but none were detected. Check `{filename_prefix:s}`")
        # else:
        #     print(f"{len(annotated)} gait events annotated, but none were detected.")
        return np.array([-999 for _ in range(len(annotated))]), np.array([]), np.array([-999 for _ in range(len(annotated))])
    if len(annotated)==0 and len(predicted)!=0:
        # print(f"No gait events annotated, but {len(predicted)} events were detected.")
        return np.array([]), np.array([-999 for _ in range(len(predicted))]), np.array([-999 for _ in range(len(predicted))])
    
    # Map every item in the list of annotated events to an item in the list of predicted events ...
    a2b = np.empty_like(annotated)
    for i in range(len(annotated)):
        imin = np.argmin(np.abs(predicted - annotated[i]))
        a2b[i] = imin
    # ... and vice versa
    b2a = np.empty_like(predicted)
    for i in range(len(predicted)):
        imin = np.argmin(np.abs(annotated - predicted[i]))
        b2a[i] = imin
    
    # If multiple items from the list of annotated events point to the same item
    # in the list of predicted events ...
    a2b_unique = np.unique(a2b)
    for i in range(len(a2b_unique)):
        indices = np.argwhere(a2b == a2b_unique[i])[:,0]
        if len(indices) > 1:
            # ... determine which one is closest to the predicted item, and
            # set the other to -999
            a2b[np.setdiff1d(indices, b2a[a2b_unique[i]])] = -999
    
    b2a_unique = np.unique(b2a)
    for i in range(len(b2a_unique)):
        indices = np.argwhere(b2a == b2a_unique[i])[:,0]
        if len(indices) > 1:
            b2a[np.setdiff1d(indices, a2b[b2a_unique[i]])] = -999
    # All valid pointers in the annotated list should have a pointer in the 
    # predicted list
    indices_a2b = np.argwhere(a2b > -999)[:,0]
    indices_b2a = np.argwhere(b2a > -999)[:,0]
    
    a2b[indices_a2b[np.argwhere(b2a[a2b[indices_a2b]] == -999)[:,0]]] = -999

    # ... and vice versa
    b2a[indices_b2a[np.argwhere(a2b[b2a[indices_b2a]]  == -999)[:,0]]] = -999
    # second round check
    indices_a2b = np.argwhere(a2b > -999)[:,0]
    a2b[indices_a2b[np.argwhere(b2a[a2b[indices_a2b]] == -999)[:,0]]] = -999

    # if len(annotated)<len(predicted): 
    #     a2b[indices_a2b[np.argwhere(b2a[a2b[indices_a2b]] == -999)[:,0]]] = -999
    
    #     # ... and vice versa
    #     b2a[indices_b2a[np.argwhere(a2b[b2a[indices_b2a]]  == -999)[:,0]]] = -999
    # elif len(annotated)==len(predicted): 
    #     a2b_old = a2b
    #     b2a_old = b2a
    #     a2b[indices_a2b[np.argwhere(b2a[a2b[indices_a2b]] == -999)[:,0]]] = -999    
    #     # ... and vice versa
    #     b2a[indices_b2a[np.argwhere(a2b[b2a[indices_b2a]]  == -999)[:,0]]] = -999
    #     if sum(a2b!=-999) != sum(b2a!=-999): # if order of operations is not right
    #         a2b = a2b_old
    #         b2a = b2a_old
    #         b2a[indices_b2a[np.argwhere(a2b[b2a[indices_b2a]]  == -999)[:,0]]] = -999

    #         a2b[indices_a2b[np.argwhere(b2a[a2b[indices_a2b]] == -999)[:,0]]] = -999
    # else: 
    #     b2a[indices_b2a[np.argwhere(a2b[b2a[indices_b2a]]  == -999)[:,0]]] = -999

    #     a2b[indices_a2b[np.argwhere(b2a[a2b[indices_a2b]] == -999)[:,0]]] = -999
    
    
    # Initial estimate of the time difference
    time_diff = predicted[b2a > -999] - annotated[a2b > -999]

    # Create local copies
    indices_a2b = a2b[a2b > -999]
    indices_b2a = b2a[b2a > -999]
    for ti in range(len(time_diff)-1, -1, -1):
        if abs(time_diff[ti]) > thr:
            a2b[indices_b2a[ti]] = -999
            b2a[indices_a2b[ti]] = -999

    # Final estimate of the time difference
    time_diff = predicted[b2a > -999] - annotated[a2b > -999] 
    return a2b, b2a, time_diff

def MetricsGaitEvents(ipksGS_,ipksDUT_,targets_2_predictions,predictions_2_targets): 
    """
    This function derives the number of missed and extra events for a given set
    of predicted and annotated events. Function also returns the time steps at
    which correct predicted events occur (with nan instead of missed events) 

    Parameters
    ----------
    ipksGS_ : ndarray
        Vector of time steps (samples) at which annotated events occur. 
    ipksDUT_ : ndarray
        Vector of time steps (samples) at which predicted events occur.
    targets_2_predictions : ndarray
        Vector of pointers from annotated to predicted. Each -999 is a missed event.
    predictions_2_targets : ndarray
        Vector of pointers from predicetd to annotated. Each -999 is an extra event.
 

    Returns
    -------
    missed : int
        Number of missed events.
    extra : int
        Number of extra events.
    predicted_aligned : ndarray
        Vector of time steps (samples) at which correct predicted events occur with nans instead of missed events

    """ 
    # the number of missed events is equal to the number of target ICs that 
    # have not a valid pointer
    missed = len(targets_2_predictions[targets_2_predictions==-999])
    # the number of extra events is equal to the number of preeicted ICs that 
    # have not a valid pointer
    extra = len(predictions_2_targets[predictions_2_targets==-999])
    # initialize array of predicted ICs with same length of array of target ICs
    predicted_aligned = np.full_like(ipksGS_,-999)
    # find indices of valid predicted ICs
    matched_events = np.argwhere(targets_2_predictions!=-999)[:,0]
    # set missed ICs to nan inside vector of predicted ICs
    predicted_aligned[matched_events] = ipksDUT_[predictions_2_targets != -999]
    
    return missed, extra, predicted_aligned

def buildDataSet(DS): 
    """
    This function extracts predictors and targets from a generic test set and
    reshapes them to fit a trained TCN model. 

    Parameters
    ----------
    DS : ndarray
        Array of annotated examples. Each row contains a 6-channels window of
        200 timesteps. The last 200 timesteps are the target label.  
    
    Returns
    -------
    x_val : ndarray
        3D array of predictors.
    y_val : ndarray
        2D array of target labels.
    """
    timesteps, input_dim = 200, 6
    #if DS is composed by one window only
    if np.ndim(DS) == 1: 
        batch_sizeDS = 1 # size of predictors array
        val_pred = DS[:1200]
        val_target = DS[1200:]
        x_val = val_pred.reshape((batch_sizeDS,timesteps,input_dim),order = 'F')
        y_val = val_target.reshape((batch_sizeDS,timesteps,1),order = 'F')
    else: 
        batch_sizeDS = DS.shape[0] # size of predictors array
        # first 1200 columns corresponds to predictors, last 200 columns corresponds to targets
        val_pred = DS[:,:1200]
        val_target = DS[:,1200:]
        # reshaping
        x_val = val_pred.reshape((batch_sizeDS,timesteps,input_dim),order = 'F')
        y_val = val_target.reshape((batch_sizeDS,timesteps,1),order = 'F')
    return x_val, y_val

def modelEvaluate(model,x,t):
    """
    This function evaluates the performance of a generic model on
    the validation data (real-world, standardized and overall). The function
    returns the percentage of extra and missed events and the mean time delay.

    Parameters
    ----------
    model : keras.engine.functional.Functional
        TCN model used for testing. 
    x : ndarray
        Array of predictors. Each row contains a 6-channels window of
        200 timesteps. 
    t : ndarray
        Array of targets. Each row contains a label window of 200 timesteps. 
        erased arguments: history,provaPath,condition, saveflag, jj
    """
    # TCN output: preds is a ndarray with shape (x.shape[0], x.shape[1], 1) and
    # values ranged between 0 and 1. Values closer to 1 denote a higher probability
    # of having a gait event (initial contact)
    preds = model.predict(x)
    # initialize arrays for results
    missedEvents = 0
    extraEvents = 0
    GSevents = 0
    Differenze = []
    ipksDUT = []
    ipksGS = []
    fs = 100 # sampling frequency (Hz)
    # loop for metrics evaluation. Each iteration takes a single window as input 
    # and returns target ICs, predicted ICs and metrics that are concatenated to
    # windows of the same micro walking bout. 
    for i in range(preds.shape[0]): # preds.shape[0] --> number of windows in the micro-walking bout
        # first sample of current window referred to the beginning of current 
        # micro-walking bout. Needed for de-stacking of windows. 
        s = i*preds.shape[1] # preds.shape[1] --> window length (default: 200) 
        # raw mono-dimensional predicted label
        predLabel = preds[i,:,0]
        # mono-dimensional target label
        targetLabel = t[i,:,0]
        # # PLOT target and predicted labels over current window
        # ax = plt.figure()
        # plt.plot(predLabel)
        # plt.plot(targetLabel)
        # plt.legend(["TCN output","Target"],loc="best")
        # plt.xlabel("Samples")
        # ax = plt.figure()
        # plt.plot(x[i,:,0])
        # plt.plot(x[i,:,1])
        # plt.plot(x[i,:,2])
        # plt.plot(targetLabel)
        # plt.xlabel("Samples")
        # plt.ylabel("Scaled accelerations")
        # plt.legend(["AP","V","ML","Predicted ICs"],loc="lower right")

        # height threshold
        min_height = 0.05 # last: 0.05
        min_prominence = 0.04 # last: 0.05
        min_distance = 40 # last: 20
        # peak detection on raw predicted label of current window
        ipksDUT_, _ = find_peaks(predLabel, height = min_height, prominence = min_prominence, distance=min_distance)
        # check to include first sample of the current window 
        if predLabel[0] >= min_height: 
            ipksDUT_ = np.concatenate((np.array([0]),ipksDUT_))
        # check to include last sample of the current window 
        if predLabel[-1] >= min_height: 
            ipksDUT_ = np.concatenate((ipksDUT_,np.array([len(predLabel)-1])))
        # find indices of target ICs of current window
        ipksGS_ = np.argwhere(targetLabel==1)[:,0]
        # return arrays of pointers and array of time differences for the current window
        targets_2_predictions, predictions_2_targets, time_diff = compare_events(ipksGS_, ipksDUT_, thr=20)
        # return number of missed events, extra events, array of time differences and time steps of predicted ICs (missed events are set to -999)
        missed, extra, ipksDUT_ = MetricsGaitEvents(ipksGS_,ipksDUT_,targets_2_predictions,predictions_2_targets)
        # update number of target events in the mWB
        GSevents = GSevents + len(ipksGS_)
        # update number of missed and extra events in the mWB
        missedEvents = missedEvents + missed
        extraEvents = extraEvents + extra
        # update array of time differecnes of the mWB
        Differenze = np.concatenate([Differenze,time_diff])
        # linearize target and predicted events 
        # convert to float (required for for nan conversion)
        ipksDUT_ = ipksDUT_.astype('float')
        # convert missed events to nan
        ipksDUT_[ipksDUT_==-999] = np.NAN
        # shift ICs in time with respect to the first sample of the current micro walking bout
        ipksGS_ = s + ipksGS_ + 1 # +1 addend is to shift from Python indexing to Matlab indexing
        ipksDUT_ = s + ipksDUT_ + 1
        # concatenate target and predicted ICs to previous target and predicted ICs of the current mWB
        ipksGS = np.concatenate((ipksGS,ipksGS_))
        ipksDUT = np.concatenate((ipksDUT,ipksDUT_))
    return extraEvents, missedEvents, ipksDUT, ipksGS

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], io.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, io.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict