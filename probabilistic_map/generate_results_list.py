"""
    generate_results_list.py
"""



# This module is in order to generate results list to a csv format file for probabilistic map generation.

# content of file path:
# ciftify path: /nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify
# subject id: /sub-M01
# second level feat folder: /MNINonLinear/Results/ses-01_task-motor/ses-01_task-motor_hp200_s4_level2.feat
# filename: /sub-M01_ses-01_task-motor_level2_zstat_Ankle-Avg_hp200_s4.dscalar.nii

# content of filename:
# if zstat and -Avg in filename, append to list

# Input: cifti_path, subject_list.csv, second_level_feat_folder_path
# Output: csv file of results list



# import modules
import os
import pandas as pd

# function: results list pipeline

def results_list_pipeline(cifti_path, subject_list_path, second_level_feat_folder_path):
    print('Generating results list...')
    results_path = []
    subject_list = pd.read_csv(subject_list_path, header = None)
    subject_list = subject_list.values.tolist()
    for subject in subject_list:
        feat_folder_path = os.path.join(cifti_path, subject[0], second_level_feat_folder_path)
        files_in_current_feat_folder_list = os.listdir(feat_folder_path)
        for filename in files_in_current_feat_folder_list:
            if 'zstat' in filename and '-Avg' in filename:
                filepath = os.path.join(feat_folder_path, filename)
                results_path.append(filepath)
    df = pd.DataFrame(results_path)
    df.to_csv('results_list.csv', header=None, index=None, columns=None)
    print('Finish!')

