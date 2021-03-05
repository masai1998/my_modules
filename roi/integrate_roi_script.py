"""
    integrate_roi.py
"""



import os
import nibabel as nib
import numpy as np

max_pmap_file = '/nfs/e2/workingshop/masai/max_pmap.nii'
Head_file = '/nfs/e2/workingshop/masai/Lh_Head_roi.nii'
Upperlimbs_file = '/nfs/e2/workingshop/masai/Lh_UpperLimbs_roi.nii'
Lowerlimbs_file = '/nfs/e2/workingshop/masai/Lh_LowerLimbs_roi.nii'

max_pmap_data = nib.load(max_pmap_file).get_fdata()
Head_data = nib.load(Head_file).get_fdata()
Upperlimbs_data = nib.load(Upperlimbs_file).get_fdata()
Lowerlimbs_data = nib.load(Lowerlimbs_file).get_fdata()

max_pmap_data = np.squeeze(max_pmap_data)
Head_data = np.squeeze(Head_data)
Upperlimbs_data = np.squeeze(Upperlimbs_data)
Lowerlimbs_data = np.squeeze(Lowerlimbs_data)

Head_max_data = np.zeros(32492)
Upperlimbs_max_data = np.zeros(32492)
Lowerlimbs_max_data = np.zeros(32492)

for i in range(32492):
    if (max_pmap_data[i] == 1) and (Head_data[i] != 0):
        Head_max_data[i] = 1
    if (max_pmap_data[i] == 2) and (Upperlimbs_data[i] != 0):
        Upperlimbs_max_data[i] = 1
    if (max_pmap_data[i] == 3) and (Lowerlimbs_data[i] != 0):
        Lowerlimbs_max_data[i] = 1

Head_max_data = Head_max_data[:, None, None]
Upperlimbs_max_data = Upperlimbs_max_data[:, None, None]
Lowerlimbs_max_data = Lowerlimbs_max_data[:, None, None]

Head_header = nib.load(Head_file).header
Head_affine = nib.load(Head_file).affine
Head_save_path = 'Head_max.nii'
Head_image = nib.Nifti2Image(Head_max_data, header=Head_header, affine=Head_affine)
nib.nifti2.save(Head_image, Head_save_path)

Upperlimbs_header = nib.load(Upperlimbs_file).header
Upperlimbs_affine = nib.load(Upperlimbs_file).affine
Upperlimbs_save_path = 'Upperlimbs_max.nii'
Upperlimbs_image = nib.Nifti2Image(Upperlimbs_max_data, header=Upperlimbs_header, affine=Upperlimbs_affine)
nib.nifti2.save(Upperlimbs_image, Upperlimbs_save_path)

Lowerlimbs_header = nib.load(Lowerlimbs_file).header
Lowerlimbs_affine = nib.load(Lowerlimbs_file).affine
Lowerlimbs_save_path = 'Lowerlimbs_max.nii'
Lowerlimbs_image = nib.Nifti2Image(Lowerlimbs_max_data, header=Lowerlimbs_header, affine=Lowerlimbs_affine)
nib.nifti2.save(Lowerlimbs_image, Lowerlimbs_save_path)