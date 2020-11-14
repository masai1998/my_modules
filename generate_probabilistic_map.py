"""
    generate_probabilistic_map.py
"""



# This module is in order to generate the probabilistic map from second level analysis results (ztate file)
# Input: task_list.csv, second_level_analysis_results_path.csv, z threshold value
# Output: "dscalar.nii" format file for each task

# import modules

import os
import numpy as np
import pandas as pd
import nibabel as nib

# function: probabilistic_map_pipeline
# workflow: 1. read task list from parameter "task_list_path", save as a pandas DataFrame
#           2. read each second level analysis results from parameter "second_level_analysis_results_folder_path"
#           3. generate binary image (a image consisted of two value such as zero and one) and save as a list
#           4. sum each list and divide by the number of participants
#           5. save probabilistic map of each tasks as "dscalar.nii" format

def probabilistic_map_pipeline(task_list_path, second_level_analysis_results_path, z_threshold_value):
    task_list = pd.read_csv(task_list_path, header = None)
    for task in task_list:
        print('Computing task: ' + task)
        temp_matrix =
        for path in second_level_analysis_results_path:



