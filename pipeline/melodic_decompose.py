"""
/nfs/m1/BrainImageNet/NaturalObject/data/bold/nifti/sub-core01/ses-ImageNet01/func/
"""

import os, subprocess, re

def melodic_decompose(args):
    fmriprep_dir = os.path.join(args.fmriprep_output, 'fmriprep')
    ica_output_dir = args.ica_output
    subject_id = args.subject
    sessions = os.listdir(os.path.join(args.nifti, 'sub-' + subject_id))
    for session_id in sessions:
        func_dir = os.listdir(os.path.join(args.nifti, 'sub-' + subject_id, session_id, 'func'))
        file_list = []
        for file in func_dir:
            if 'bold.nii.gz' in file:
                file_list.append(file)
        run_list = []
        for filename in file_list:
            run_list.append(re.findall("task-object_(.+?)_bold", str))
        for run_id in run_list:
            func_data = os.path.join(fmriprep_dir, subject_id, session_id, 'func',
                                     subject_id + '_' + session_id + '_' + 'task-motor' + '_' + run_id + '_space-T1w_desc-preproc_bold.nii.gz')
            ica_output = os.path.join(ica_output_dir, subject_id, session_id, run_id + '.ica')
            melodic_command = ' '.join(['melodic', '-i', func_data, '-o', ica_output,
                                        '-v --nobet --bgthreshold=1 --tr=2 -d 0 --mmthresh=0.5 --report'])
            try:
                subprocess.check_call(melodic_command, shell=True)
            except subprocess.CalledProcessError:
                raise Exception('MELODIC: Error happened in subject {}'.format(subject_id))



