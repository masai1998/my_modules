"""
    task_analysis.py
"""



import os
import numpy as np
import  pandas as pd
import subprocess



class task_analysis(object):

    def __init__(self, raw_data_dir, ciftify_dir, subject_list, fsf_template_dir):
        self.raw_data_dir = raw_data_dir
        self.ciftify_dir = ciftify_dir
        self.subject_list = subject_list
        self.fsf_template_dir = fsf_template_dir

    def prepare_fsf(self):
        level1_fsf_file = os.path.join(self.fsf_dir, 'level1.fsf')

#        level2_fsf_file = os.path.join(self.fsf_dir, 'level2.fsf')

        for subject_id in self.subject_list:
            results_dir = os.path.join(self.ciftify_dir, subject_id, 'MNINonLinear', 'Results')
            with open(os.path.join(self.raw_data_dir, subject_id, 'ses-01', 'tmp', 'run_info', 'motor.rlf'), 'r') as f:
                runs_id = f.read().splitlines()
#            fsflevel2_outdir = os.path.join(results_dir, 'ses-01_task-motor_level2_test')
#            cpfsf2_command = ' '.join(['cp', level2_fsf_file, os.path.join(fsflevel2_outdir, ses_id + '_' + 'task-' + self.task + '_hp200_s4_level2.fsf')])
#            subprocess.call(cpfsf2_command, shell=True)
#            self._modify_fsf2(os.path.join(fsflevel2_outdir, ses_id + '_' + 'task-' + self.task + '_hp200_s4_level2.fsf'), runs_id)
            for run_id in runs_id:
                level1_fsf_file_outdir = os.path.join(results_dir, 'ses-01_task-motor_run-' + run_id)
                if not os.path.exists(level1_fsf_file_outdir):
                    os.mkdir(level1_fsf_file_outdir)
                cpfsf1_command = ' '.join(['cp', level1_fsf_file, os.path.join(fsflevel1_outdir, ses_id + '_' + 'task-' + self.task + '_' + 'run-' + run_id + '_hp200_s4_level1.fsf')])
                subprocess.call(cpfsf1_command, shell=True)

