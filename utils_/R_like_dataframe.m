function [results, info] = R_like_dataframe(TimeMeasure1)
% R_LIKE_DATAFRAME Function to convert the output of the gait events
% detection block to a format for R
% -------------------------------------------------------------------------
% Author: Paolo Tasca (Politecnico di Torino, paolo.tasca@polito.it)
% Version history:
%   v1:                 Mat 12th 2023
% -------------------------------------------------------------------------
% Inputs:
%   data:               INDIP data (type: 1x1 struct)
% Outputs:
%   pre_processed_data: INDIP pre-processed data (type: 1x1 struct)
% -------------------------------------------------------------------------

struct_test_names = fieldnames(TimeMeasure1); % Test names. es. 'Test4'
for nTest = 1:length(struct_test_names)
    struct_trial_names = fieldnames(TimeMeasure1.(struct_test_names{nTest})); % Trial names. es. 'Trial1'
    for nTrial = 1:length(struct_trial_names)
        mWBs = TimeMeasure1.(struct_test_names{nTest}).(struct_trial_names{nTrial}).Standards.INDIP.MicroWB;
        if size(mWBs)==1
            [mWB_array_,info_mWB_] = extract_(mWBs);
            results.(struct_test_names{nTest}).(struct_trial_names{nTrial}) = mWB_array_;
            info.(struct_test_names{nTest}).(struct_trial_names{nTrial}) = info_mWB_;
        else
            for mWBi = 1:size(mWBs,1)
                mWB = mWBs{mWBi,1};
                [mWB_array_,info_mWB_] = extract_(mWB);
                results.(struct_test_names{nTest}).(struct_trial_names{nTrial}) = mWB_array_;
                info.(struct_test_names{nTest}).(struct_trial_names{nTrial}) = info_mWB_;
            end
        end
    end
end