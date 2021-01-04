"""
    max_pmap.py
"""



import os
import numpy as np
import pandas as pd
import nibabel as nib

Head_file = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/probabilistic_map/Head.dscalar.nii'
Upperlimbs_file = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/probabilistic_map/UpperLimbs.dscalar.nii'
Lowerlimbs_file = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/probabilistic_map/LowerLimbs.dscalar.nii'

Head_data = nib.load(Head_file).get_fdata()
Upperlimbs_data = nib.load(Upperlimbs_file).get_fdata()
Lowerlimbs_data = nib.load(Lowerlimbs_file).get_fdata()

# 1, 91282

first_column = np.zeros(91282).reshape((-1,1))
Head_data = np.where(Head_data > 0.25, Head_data, 0).reshape((-1,1))
Upperlimbs_data = np.where(Upperlimbs_data > 0.25, Upperlimbs_data, 0).reshape((-1,1))
Lowerlimbs_data = np.where(Lowerlimbs_data > 0.25, Lowerlimbs_data, 0).reshape((-1,1))
pmap_matrix = np.c_[first_column, Head_data, Upperlimbs_data, Lowerlimbs_data]

max_pmap_data = np.argmax(pmap_matrix, axis = 1).reshape((1,-1))

header = nib.load(Head_file).header
save_path = 'pmap.dscalar.nii'
image = nib.Cifti2Image(max_pmap_data, header)
nib.cifti2.save(image, save_path)