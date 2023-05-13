function [events,info_WBs] = extract_(struct_data)
%EXTRACT_ Put data in struct into array
% -------------------------------------------------------------------------
% Author: Paolo Tasca (Politecnico di Torino, paolo.tasca@polito.it)
% Version history: 
%   v1:                 Mat 12th 2023
% -------------------------------------------------------------------------
% Inputs: 
%   struct_data:               INDIP mWB data (type: 1x1 struct)
% Outputs: 
%   events:                    predicted and target ICs (type: double array)
%   info_WBs:                  number of total, missed and extra events for
%                              the current mWB
% -------------------------------------------------------------------------
t_ICs = struct_data.Target_Initial_Contact_Events; % target ICs
p_ICs = struct_data.Predicted_Initial_Contact_Events; % predicted ICs
extra = struct_data.ExtraEvents; % number of extra events for current mWB
missed = struct_data.MissedEvents; % number of missed events for current mWB
tot = length(t_ICs); % number of target events for current mWB
events = [t_ICs,p_ICs]; 
info_WBs = [extra,missed,tot]; 
end

