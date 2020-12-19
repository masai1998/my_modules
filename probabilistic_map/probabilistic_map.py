"""
    probabilistic_map.py
"""



import os
import numpy as np
import nibabel as nib

class probabilistic_map(object):

    def __init__(self, raw_data_dir, ciftify_data_dir, contrast_list, task, z_threshold, header):
        self.raw_data_dir = raw_data_dir
        self.ciftify_data_dir = ciftify_data_dir
        self.contrast_list = contrast_list
        self.task = task
        self.z_threshold = z_threshold
        self.header = header

    def generate_map(self):

        # Make the directory of probabilistic maps

        probabilistic_map_dir = os.path.join(self.ciftify_data_dir, '..', 'probabilistic_map')
        if not os.path.exists(probabilistic_map_dir):
            os.makedirs(probabilistic_map_dir)

        # Read subjects information

        subject_list = []
        all_ciftify_folders = os.listdir(self.ciftify_data_dir)
        for foldername in all_ciftify_folders:
            if 'sub-M' in foldername:
                subject_list.append(foldername)
        subject_num = len(subject_list)

        # Read contrasts

        contrast_dict = {}
        for contrast in self.contrast_list:
            contrast_dict[contrast] = []

        # Read data of every contrasts

        for subject in subject_list:
            print('Reading subject {} ...'.format(subject))
            raw_subject_dir = os.path.join(self.raw_data_dir, subject)
            session_list = os.listdir(raw_subject_dir)
            for session in session_list:
                print('Reading session {} ...'.format(session))
                results_dir = os.path.join(self.ciftify_data_dir, subject, 'MNINonLinear', 'Results',
                                           session + '_' + 'task-' + self.task,
                                           session + '_' + 'task-' + self.task + '_' + 'hp200' + '_' + 's4' + '_' + 'level2' + '.feat')
                for contrast_name in contrast_dict.keys():
                    print('Reading contrast {} ...'.format(contrast_name))
                    zstat_file = os.path.join(results_dir,
                                              subject + '_' + session + '_' + 'task-' + self.task + '_' + 'level2' + '_' + 'zstat' + '_' + contrast_name + '_' + 'hp200' + '_' + 's4' + '.dscalar.nii')
                    current_data = nib.load(zstat_file).get_fdata()
                    current_data_threshold = np.where(current_data > self.z_threshold, 1, 0)
                    contrast_dict[contrast_name].append(current_data_threshold)

        # Calculate every contrast to probabilistic style data

        for contrast_name in contrast_dict.keys():
            print('Calculating contrast {} ...'.format(contrast_name))
            contrast_dict[contrast_name] = (sum(contrast_dict[contrast_name])) / subject_num

        # Save probabilistic maps

        for contrast_name in contrast_dict.keys():
            print('Saving probabilistic map of {} ...'.format(contrast_name))
            save_path = os.path.join(probabilistic_map_dir, contrast_name + '.dscalar.nii')
            image = nib.Cifti2Image(contrast_dict[contrast_name], self.header)
            nib.cifti2.save(image, save_path)

        print(' ########## Work Completed ########## ')



if __name__ == '__main__':

    raw_data_dir = '/nfs/e4/function_guided_resection/MotorMapping/'
    ciftify_data_dir = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify/'
    contrast_list = ['Head', 'UpperLimbs', 'LowerLimbs']
    task = 'motor'
    z_threshold = 4.7534
    header = nib.load('/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify/sub-M24/MNINonLinear/Results/ses-01_task-motor/ses-01_task-motor_hp200_s4_level2.feat/sub-M24_ses-01_task-motor_level2_zstat_Head_hp200_s4.dscalar.nii').header

    probabilistic_map = probabilistic_map(raw_data_dir, ciftify_data_dir, contrast_list, task, z_threshold, header)
    probabilistic_map.generate_map()








