"""
    clusters.py
"""



import os
import nibabel as nib
import numpy as np
from sklearn.cluster import KMeans

def prepare_image(image_file, z_threshold):
    image = nib.load(image_file)
    data = image.get_fdata()
    data = np.where(data > z_threshold, data, 0)
    header = image.header
    return data, header

def clusters(data, k):
    #data = [[z] for z in data.reshape(1, -1)]
    data = data.reshape(1, -1)
    km = KMeans(n_clusters=k)
    km.fit(data)
    print(km.cluster_centers)


def run(image_file, z_threshold, k):
    data, header = prepare_image(image_file, z_threshold)
    clusters(data, k)

if __name__ == '__main__':
    image_file = r'C:\Users\10719\Desktop\test\24\sub-M24_ses-01_task-motor_level2_zstat_Head_hp200_s4.dscalar.nii'
    z_threshold = 3.3
    k = 2
    run(image_file, z_threshold, k)
