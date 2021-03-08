"""
fmriprep-docker
/nfs/e4/function_guided_resection/MotorMapping
/nfs/e4/function_guided_resection/MotorMapping/derivatives/fmriprep_test
participant
-w /nfs/e4/function_guided_resection/fmriprep_tmp_ms
--participant_label M01
--output-space T1w
--skip-bids-validation
--fs-license-file /usr/local/neurosoft/freesurfer/license.txt
"""

import subprocess

def run_fmriprep(args):
    fmriprep_command = ''.join('fmriprep-docker',
                               args.nifti,
                               args.fmriprep_output,
                               'participant', '-w', args.fmriprep_workdir,
                               '--participant_label', args.subject,
                               '--output-space', 'T1w',
                               '--skip-bids-validation',
                               '--fs-license-file', '/usr/local/neurosoft/freesurfer/license.txt')
    try:
        subprocess.check_call(fmriprep_command, shell=True)
    except subprocess.CalledProcessError:
        raise Exception('FMRIPREP: Error happened in subject {}'.format(args.subject))