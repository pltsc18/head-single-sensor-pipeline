% main2.m
% -------------------------------------------------------------------------
% Author: Paolo Tasca (Politecnico di Torino, paolo.tasca@polito.it)
% Version history: 
%   v1:                 Mat 12th 2023
% -------------------------------------------------------------------------
% Main code for standardizing output of the gait events detection block (to
% be ready for evaluation in R)
clear all; close all; clc; 
%Stampa nella command window
fprintf('\n Program for data standardization \n\n');
fprintf('\n Processing... \n\n');
%% Data loading
% current folder
current_folder = pwd; 
% add utils_ folder to path
addpath(genpath([current_folder filesep 'utils_']))
% subject name (CHANGE WITH DESIRED SUBJECT NAME)
subID = '0001'; 
% loading output of model
load([current_folder filesep subID filesep 'output.mat']); 
%% Organize results into arrays for R processing
[results, info] = R_like_dataframe(TimeMeasure1); 
%% Save
save([current_folder filesep subID filesep 'output_for_R.mat'],'results', 'info'); 
fprintf('\n Done! \n\n');



