"""
    generate_probabilistic_map.py
"""



# This module is in order to generate the probabilistic map from second level analysis results (ztate file)
# Input: task_list.csv, results_list.csv, z threshold value, participants_number
# Output: "dscalar.nii" format file for each task

# import modules

import os
import numpy as np
import pandas as pd
import nibabel as nib

# function: probabilistic map pipeline

def probabilistic_map_pipeline(task_list_path, results_list_path, z_threshold_value, participants_number):
    task_list = pd.read_csv(task_list_path, header = None)
    results_list = pd.read_csv(results_list_path, header = None)
    if not os.path.exists('probabilistic_map'):
        print('Creating a folder in current path named "probabilistic_map".')
        os.mkdir('probabilistic_map')
    else:
        print('The folder "probabilistic_map" is exist!')
    for task in task_list:
        print('Processing task is: ' + task)
        task_in_results_list = find_task_in_results_path(task, results_list)
        print('Computing task...')
        task_data , task_header = compute_probabilistic_map_of_one_task(task_in_results_list, z_threshold_value, participants_number)
        print('Saving as ' + task + '.dscalar.nii')
        save_to_dscalar(task, task_data, task_header)
    print('Finish!')

# function: find task in results path

def find_task_in_results_path(task, results_list):
    task_in_results_list = []
    for path in results_list:
        if task in path:
            task_in_results_list.append(path)
    return task_in_results_list

# function: compute probabilistic map of one task

def compute_probabilistic_map_of_one_task(task_in_results_list, z_threshold_value, participants_number):
    initial_image = nib.load(task_in_results_list[0])
    task_header = initial_image.header
    task_data_original = initial_image.get_fdata()
    task_data_binary = np.where(task_data_original > z_threshold_value, 1, 0)
    for path in task_in_results_list[1:]:
        temp_image = nib.load(path)
        temp_data_original = temp_image.get_fdata()
        temp_data_binary = np.where(temp_data_original > z_threshold_value, 1, 0)
        task_data_binary += temp_data_binary
    task_data = task_data_binary / participants_number
    return task_data , task_header

# function: save to descalar

def save_to_dscalar(task, task_data, task_header):
    filename = task + '.dscalar.nii'
    filepath = os.path.join('probabilistic_map', filename)
    temp_image = nib.Cifti2Image(task_data, task_header)
    nib.cifti2.save(temp_image, filepath)