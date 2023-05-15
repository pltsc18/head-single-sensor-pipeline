# Gait events detection based on a single H-IMU
Repository contains Matlab and Python codes and assets for estimating initial contact (IC) events from raw 3D acceleration and angular rate recorded by a single head-mounted IMU (H-IMU). Data of subject must be saved according the Mobilise-D structure (https://www.mobilise-d.eu/data). 
# Requirements
- Matlab 2020b (or more recent)
- Python 3.9 (or more recent)
- A Python IDE (suggested: Spyder)
- Python packages: os, numpy, matplotlib, tensorflow, scipy, tcn. To install a Python package run "pip install \<package name\>" in the console.

Installing Anaconda (https://www.anaconda.com/download) is suggested, as it conveniently installs Python, the Jupyter Notebook, and other commonly used packages for scientific computing and data science (e.g. Spyder). Alternatively, you can separately install Python first (https://www.python.org/downloads/) and then install an IDE (e.g. Spyder: https://www.spyder-ide.org/; Python IDLE: https://www.python.org/, etc...). 
# Before running
Download and unzip the repository. Then: 
1. Edit line 21 of *main.m* by declaring variable *subjects_folder* equal to the path (type: string) to the folder where subjects folders are stored i.e. folder that contains the sub-folders named "0001", "0002", "0003", etc...
2. Edit line 24 of *main.m* by declaring variable *subID* equal to the name (type: string) of the tested subject folder (e.g. "0001").
3. Edit line 19 of *utils_/label_data.m* and line 13 of *utils_/pre_process.m* by declaring variable *first_test* equal to the first test (type: double) present in *data.mat* that is to be processed
4. Edit line 19 of *main2.py* by declaring variable *subID* equal to the name (type: string) of the tested subject folder (e.g. "0001").
# Run pipeline
After having done the above listed operations, do the following: 
1. Open Matlab and set the downloaded repository as your current directory
2. Open and run *main.m*
3. Verify that a file named *data.mat* has been written in a folder named "000x" in the working directory
4. Open your Python IDE
5. Open and run *main.py*
6. Verify that a file named *output.mat* has been written in a folder named "000x" in the working directory
7. Open and run *main2.py*
8. Verify that a file named *output_for_R.mat* has been written in a folder named "000x" in the working directory



