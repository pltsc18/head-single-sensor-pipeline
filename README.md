# Gait events detection based on a single H-IMU
Repository contains Matlab and Python codes and assets for estimating initial contact (IC) events from raw 3D acceleration and angular rate recorded by a single head-mounted IMU (H-IMU). Data of subject must be saved according the Mobilise-D structure (https://www.mobilise-d.eu/data). 
# Requirements
- Matlab 2020b (or more recent)
- Python 3.9 (or more recent)
- A Python IDE 
- Python packages (to install a Python package run "pip install \<package name\>" in the console.): os, numpy, matplotlib, tensorflow, scipy, tcn, xlswriter

Installing Anaconda (https://www.anaconda.com/download) is suggested, as it conveniently installs Python, the Jupyter Notebook, and other commonly used packages for scientific computing and data science (e.g. Spyder). Alternatively, you can separately install Python first (https://www.python.org/downloads/) and then install an IDE (e.g. Spyder: https://www.spyder-ide.org/; Python IDLE: https://www.python.org/, etc...). 
# Before running
1. Edit line 21 of *main.m* by declaring variable *subjects_folder* equal to the path (type: string) to the folder where subjects folders are stored i.e. folder that contains the sub-folders named "0001", "0002", "0003", etc...
2. Edit line 24 of *main.m* by declaring variable *subID* equal to the name (type: string) of the subject folder (e.g. "0001").
3. Edit line 19 of *label_data.m* and line 13 of *pre_process.m* by declaring variable *first_test* equal to the first test (type: double) present in *data.mat* that is to be processed
# Run pipeline
After having done the above listed operations, do the following: 
1. Download the repository (namely "working directory")
2. Open Matlab
3. Open and run *main.m*
4. Verify that a folder named "000x" has been written in the working directory
5. Open your Python IDE
6. Run *main.py*
7. Upload processed folders to the "Output" folder. When uploading, choose the option "Create a new branch for this commit and start a pull request".


