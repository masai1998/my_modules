"""
    clear.py
"""



import os
import shutil

def clear(ciftify_folder, subject_id, run_id):
    # clear level1 files
    level1_folder = os.path.join(ciftify_folder, subject_id, 'MNINonLinear/Results', 'ses-01_task-motor_run-' + run_id)
    level1_files = os.listdir(level1_folder)
    for file in level1_files:
        if file.endswith('.fsf'):
            fsf_filename = file
            fsf_file = os.path.join(level1_folder, fsf_filename)
            os.remove(fsf_file)
        if file.endswith('.feat'):
            feat_foldername = file
            feat_folder = os.path.join(level1_folder, feat_foldername)
            shutil.rmtree(feat_folder)
    # clear level2 folder
    level2_folder = os.path.join(ciftify_folder, subject_id, 'MNINonLinear/Results/ses-01_task-motor')
    level2_files = os.listdir(level2_folder)
    for file in level2_files:
        if file.endswith('.fsf'):
            fsf_filename = file
            fsf_file = os.path.join(level2_folder, fsf_filename)
            os.remove(fsf_file)
        if file.endswith('.feat'):
            feat_foldername = file
            feat_folder = os.path.join(level2_folder, feat_foldername)
            shutil.rmtree(feat_folder)

if __name__ == '__main__':
    #ciftify_folder = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify/'
    ciftify_folder = '/nfs/e2/workingshop/masai/test/hcp_pipeline/ciftify/'
    subject_list = []
    run_list = []

    # load subject id
    ciftify_folder_list = os.listdir(ciftify_folder)
    for folder in ciftify_folder_list:
        if 'sub-M' in folder:
            subject_list.append(folder)

    for sub in subject_list:
        # load run id
        with open(os.path.join('/nfs/e4/function_guided_resection/MotorMapping' , sub, 'ses-01/tmp/run_info/motor.rlf'), 'r') as f:
            runs_id = f.read().splitlines()
        for run_id in runs_id:
            clear(ciftify_folder, sub, run_id)
            print(sub + ' finish!')
