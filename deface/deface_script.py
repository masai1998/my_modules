"""
    deface_script.py
"""



# import modules

import os
import pandas as pd
import subprocess

# A script in order to process deface of motor mapping anatomical images using pydeface

# get anatomical images list
# analyze the path
# the path of sub-M01 is "/nfs/e4/function_guided_resection/MotorMapping/ # sub-M01/ # ses-01/anat/ sub-M01 _ses-01_run-12_T1w.nii.gz"

image_path_list = []

subject_list = []
subject_df = pd.read_csv('/nfs/e2/workingshop/masai/probabilistic_map/pipeline/subject_list.csv', header = None)
temp_df = subject_df.values.tolist()
for i in temp_df:
    subject_list.append(i[0])
#print(subject_list)

for subj in subject_list:
    temp_path = os.path.join('/nfs/e4/function_guided_resection/MotorMapping', subj, 'ses-01/anat')
    temp_list = os.listdir(temp_path)
    for path in temp_list:
        if path.endswith('.nii.gz'):
            image_path_list.append(os.path.join(temp_path, path))
#print(image_path_list)

for path in image_path_list:
    pydeface_command = 'pydeface ' + path
    try:
        subprocess.check_call(pydeface_command, shell=True)
    except subprocess.CalledProcessError:
        raise Exception('ERROR!!!')
