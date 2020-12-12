"""
    integrate_roi.py
"""



import os
import nibabel as nib
import numpy as np

class integration(object):

    def __init__(self, roi_dir, header, savename):
        self.roi_dir = roi_dir
        self.header = header
        self.savename = savename

    def integrate_roi(self):

        # read and integrate data

        data = None
        roi_files_list = os.listdir(self.roi_dir)
        for roi_file in roi_files_list:
            roi_file_path = os.path.join(self.roi_dir, roi_file)
            temp_data = nib.load(roi_file_path).get_fdata
            data = data + temp_data

        # save roi file

        integrated_file_path = os.path.join(self.roi_dir, self.savename, '.nii.gz')
        image = nib.Nifti2Image(data, self.header)
        nib.nifti2.save(image, integrated_file_path)



if __name__ == '__main__':
    roi_dir = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/roi/Head'
    header = nib.load('/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/roi/Head/L_Head_z=4.7_p=0.25_region-a.nii.gz').header
    savename = 'L_Head_z=4.7_p=0.25'

    integration(roi_dir, header, savename)
    integration.integrate_roi()
