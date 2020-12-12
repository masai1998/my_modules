"""
    integrate_roi.py
"""



import os
import nibabel as nib
import numpy as np

Head_roi = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/roi/Head'
a_path = os.path.join(Head_roi, 'L_Head_z=4.7_p=0.25_region-a.nii.gz')
b_path = os.path.join(Head_roi, 'L_Head_z=4.7_p=0.25_region-b.nii.gz')
c_path = os.path.join(Head_roi, 'L_Head_z=4.7_p=0.25_region-c.nii.gz')
d_path = os.path.join(Head_roi, 'L_Head_z=4.7_p=0.25_region-d.nii.gz')

a = nib.load(a_path).get_fdata()
b = nib.load(b_path).get_fdata()
c = nib.load(c_path).get_fdata()
d = nib.load(d_path).get_fdata()

header = nib.load(a_path).head

data = a + b+ c + d

image = nib.Nifti1Image(data, header)
nib.save(image, Head_roi + 'L_Head_z=4.7_p=0.25.nii.gz')

