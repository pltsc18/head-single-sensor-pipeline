# Gait events detection based on a single H-IMU
Repository contains Matlab and Python codes and assets for estimating initial contact (IC) events from raw 3D acceleration and angular rate recorded by a single head-mounted IMU (H-IMU). Data of subject must be saved according the Mobilise-D structure (https://www.mobilise-d.eu/data). 
# Before running the codes
1. Edit line 21 of *main.m* by declaring variable *subjects_folder* equal to the path (type: string) to the folder where subjects folders are stored i.e. folder that contains the sub-folders named "0001", "0002", "0003", ecc...
2. Edit line 24 of *main.m* by declaring variable *subID* equal to the name (type: string) of the subject folder (e.g. "0001").
3. Edit line 19 of *label_data.m* and line 13 of *pre_process.m* by declaring variable *first_test* equal to the first test (type: double) present in *data.mat* that is to be processed
# Execute pipeline
After having done the above listed operations, do the following: 
1. Run *main.m*
2. Run *main.py*
3. Upload processed folders to the "Output" folder


