"""
    generate_probabilistic_map.py
"""



import nibabel as nib
import numpy as np
import os



# input parameters !!! no sub24 , sub39 , sub25 , sub38 !!!

print('input parameters...')

subject_id = ['sub-M24','sub-M39','sub-M25','sub-M38','sub-M01','sub-M08','sub-M16','sub-M32','sub-M48','sub-M55','sub-M62','sub-M02','sub-M09','sub-M17','sub-M33','sub-M42','sub-M49','sub-M56','sub-M63','sub-M03','sub-M10','sub-M18','sub-M26','sub-M34','sub-M43','sub-M50','sub-M57','sub-M65','sub-M04','sub-M11','sub-M20','sub-M27','sub-M35','sub-M44','sub-M51','sub-M58','sub-M66','sub-M05','sub-M12','sub-M21','sub-M29','sub-M36','sub-M45','sub-M52','sub-M59','sub-M67','sub-M06','sub-M13','sub-M22','sub-M30','sub-M37','sub-M46','sub-M53','sub-M60','sub-M68','sub-M07','sub-M14','sub-M23','sub-M31','sub-M47','sub-M54','sub-M61']
task_id = ['Toe', 'Ankle', 'LeftLeg', 'RightLeg', 'Finger', 'Wrist', 'Forearm', 'Upperarm', 'Jaw', 'Lip', 'Tongue', 'Eye']
data_input = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify'
data_output = '/nfs/e2/workingshop/masai/probabilistic_map_output/'

# read level2 data & transform

print('read and transform...')

Toe = []
Ankle = []
LeftLeg = []
RightLeg = []
Finger = []
Wrist = []
Forearm = []
Upperarm = []
Jaw = []
Lip = []
Tongue = []
Eye = []

for subject in subject_id:
    print('reading ' + subject + '...')
    subject_path = os.path.join(data_input, subject, 'MNINonLinear/Results/ses-01_task-motor/ses-01_task-motor_hp200_s4_level2.feat')
    for task in task_id:
        zstat_file_name = subject +'_ses-01_task-motor_level2_cope_' + task + '-Avg_hp200_s4.dscalar.nii'
        zstat_file_path = os.path.join(subject_path, zstat_file_name)
        temp_data = nib.load(zstat_file_path).get_fdata()
        temp_data = np.where(temp_data > 3, 1, 0)
        if task == 'Toe':
            Toe.append(temp_data)
        if task == 'Ankle':
            Ankle.append(temp_data)
        if task == 'LeftLeg':
            LeftLeg.append(temp_data)
        if task == 'RightLeg':
            RightLeg.append(temp_data)
        if task == 'Finger':
            Finger.append(temp_data)
        if task == 'Wrist':
            Wrist.append(temp_data)
        if task == 'Forearm':
            Forearm.append(temp_data)
        if task == 'Upperarm':
            Upperarm.append(temp_data)
        if task == 'Jaw':
            Jaw.append(temp_data)
        if task == 'Lip':
            Lip.append(temp_data)
        if task == 'Tongue':
            Tongue.append(temp_data)
        if task == 'Eye':
            Eye.append(temp_data)

# sum same conditions

print('sum 62 subjects...')

Toe = (sum(Toe)) / 58
Ankle = (sum(Ankle)) / 58
LeftLeg = (sum(LeftLeg)) / 58
RightLeg = (sum(RightLeg)) / 58
Finger = (sum(Finger)) / 58
Wrist = (sum(Wrist)) / 58
Forearm = (sum(Forearm)) / 58
Upperarm = (sum(Upperarm)) / 58
Jaw = (sum(Jaw)) / 58
Lip = (sum(Lip)) / 58
Tongue = (sum(Tongue)) / 58
Eye = (sum(Eye)) / 58

# save probabilistic map

print('save to image files...')

for task in task_id:
    filepath = data_output + task + '.dscalar.nii'
    header = nib.load('/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify/sub-M01/MNINonLinear/Results/ses-01_task-motor/ses-01_task-motor_hp200_s4_level2.feat/sub-M01_ses-01_task-motor_level2_cope_Ankle-Avg_hp200_s4.dscalar.nii').header
    if task == 'Toe':
        image = nib.Cifti2Image(Toe, header)
    if task == 'Ankle':
        image = nib.Cifti2Image(Ankle, header)
    if task == 'LeftLeg':
        image = nib.Cifti2Image(LeftLeg, header)
    if task == 'RightLeg':
        image = nib.Cifti2Image(RightLeg, header)
    if task == 'Finger':
        image = nib.Cifti2Image(Finger, header)
    if task == 'Wrist':
        image = nib.Cifti2Image(Wrist, header)
    if task == 'Forearm':
        image = nib.Cifti2Image(Forearm, header)
    if task == 'Upperarm':
        image = nib.Cifti2Image(Upperarm, header)
    if task == 'Jaw':
        image = nib.Cifti2Image(Jaw, header)
    if task == 'Lip':
        image = nib.Cifti2Image(Lip, header)
    if task == 'Tongue':
        image = nib.Cifti2Image(Tongue, header)
    if task == 'Eye':
        image = nib.Cifti2Image(Eye, header)
    nib.cifti2.save(image, filepath)
