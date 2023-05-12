function pre_processed_data = pre_process(data)
% PRE_PROCESS Function to pre-process data. 
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
    first_test = 3; % CHANGE WITH THE NUMBER OF THE FIRST ACQUISITION
    % Returning cell array with the names of each test
    struct_test_names = fieldnames(data.TimeMeasure1); % Test names. es. 'Test4'
    % Coefficients of low-pass filter
    fCutoff = 5; fStop = 10; % pass-band and stop-band frequencies (Hz)
    % Parameters for windowing
    winSize = 200; % size of the windows (samples)
    overlap = 0; % number of overlapped samples. TRS: 100, TS: 0
    [b,a] = LowPassFilter(fCutoff,fStop); % filter design
    for nTest = first_test:length(struct_test_names)
        % Returning cell array with the names of each trial
        struct_trial_names = fieldnames(data.TimeMeasure1.(struct_test_names{nTest})); % Trial names. es. 'Trial1'
        for nTrial = 1:length(struct_trial_names)
            % filtering and normalization of trial data
            pred = pre_process_trial(data,b,a,nTest,nTrial);
            % add pred to the structure as a new field in the Head sub-field
            data.TimeMeasure1.(['Test',num2str(nTest)]).(['Trial',num2str(nTrial)]).SU_INDIP.Head.pred_processed = pred;
        end
    end
    % target response real-world gait
    pre_processed_data = label_data(data,winSize,overlap);
end