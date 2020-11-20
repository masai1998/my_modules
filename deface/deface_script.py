"""
    deface_script.py
"""



import os
import subprocess

# A script in order to process deface of motor mapping anatomical images using pydeface

# get anatomical images list
# analyze the path
# the path of sub-M01 is "/nfs/e4/function_guided_resection/MotorMapping/ # sub-M01/ # ses-01/anat/ sub-M01 _ses-01_run-12_T1w.nii.gz"

image_path_list = []

subject_list = ['sub-M24','sub-M39','sub-M25','sub-M38','sub-M01','sub-M08','sub-M16','sub-M32','sub-M48','sub-M55','sub-M62','sub-M02','sub-M09','sub-M17','sub-M33','sub-M42','sub-M49','sub-M56','sub-M63','sub-M03','sub-M10','sub-M18','sub-M26','sub-M34','sub-M43','sub-M50','sub-M57','sub-M65','sub-M04','sub-M11','sub-M20','sub-M27','sub-M35','sub-M44','sub-M51','sub-M58','sub-M66','sub-M05','sub-M12','sub-M21','sub-M29','sub-M36','sub-M45','sub-M52','sub-M59','sub-M67','sub-M06','sub-M13','sub-M22','sub-M30','sub-M37','sub-M46','sub-M53','sub-M60','sub-M68','sub-M07','sub-M14','sub-M23','sub-M31','sub-M47','sub-M54','sub-M61']

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
