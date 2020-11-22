"""
    deface.py
"""



import os
import subprocess

class deface(object):

    def __init__(self, raw_data_dir):
        self.raw_data_dir = raw_data_dir

    def _prepare_input_parameters(self):
        anat_image_list = []
        subject_list = []
        raw_data_dir_folder_list = os.listdir(self.raw_data_dir)
        for folder in raw_data_dir_folder_list:
            if 'sub-M' in folder:
                subject_list.append(folder)
        session_id_list = os.listdir(os.path.join(raw_data_dir_folder_list, subject_list[0]))
        for subject in subject_list:
            for session in session_id_list:
                anat_path = os.path.join(raw_data_dir_folder_list, subject, session, 'anat')
                anat_file_list = os.listdir(anat_path)
                for file in anat_file_list:
                    if file.endswith('.nii.gz'):
                        anat_image_list.append(os.path.join(anat_path, file))
        return anat_image_list

    def run_deface(self):
        anat_image_list = self._prepare_input_parameters()
        for image in anat_image_list:
            pydeface_command = 'pydeface' + image
            subprocess.check_call(pydeface_command, shell=True)