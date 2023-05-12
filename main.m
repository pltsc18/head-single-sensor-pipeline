% main.m
% -------------------------------------------------------------------------
% Author: Paolo Tasca (Politecnico di Torino, paolo.tasca@polito.it)
% Version history: 
%   v1:                 Mat 12th 2023
% -------------------------------------------------------------------------
% Main code for pre-processing data saved in Mobilised-D struct
clear all; close all; clc;
%Stampa nella command window
fprintf('\n Program for data pre-processing \n\n');
fprintf('\n Performed pre-processing operations: \n');
fprintf('- Low-pass filtering (cutoff: 5 Hz) \n');
fprintf('- Z-score normalization (each trial is scaled using its mean and STD) \n');
fprintf('- Partitioning into equal-length windows (200 samples, 0 overlap) \n');
%% Data loading
% current folder
current_folder = pwd; 
% add utils_ folder to path
addpath(genpath([current_folder filesep 'utils_']))
% path to the folder that contains sub-folders of subjects (CHANGE HERE)
subjects_folder = 'G:\Drive condivisi\Borsa Paolo Tasca\Acquisizioni testa\Standardized'; 
% subjects_folder = "..."; 
% subject name (CHANGE WITH DESIRED SUBJECT NAME)
subID = '0001'; 
% path to current subject's data folder
sub_path = [subjects_folder filesep subID]; 
load([sub_path filesep 'Mobility Test' filesep 'Results' filesep 'data.mat'])
%% Pre-processing
pre_processed_data = pre_process(data); 
%% Saving
% create folder for storing pre-processed data
save_path = [current_folder filesep subID]; 
mkdir(save_path)
save([save_path filesep 'data.mat'],'pre_processed_data')