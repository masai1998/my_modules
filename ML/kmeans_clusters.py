"""
    kmeans_clusters.py
"""



import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# class clusters(object):
#
#     def __init__(self, data_dir, subject_list, contrast_name, clusters_num, iteration_times, ):


first_column = np.random.random(9).reshape((-1,1))
second_column = np.random.random(9).reshape((-1,1))
third_column = np.random.random(9).reshape((-1,1))
X = np.c_[first_column, second_column, third_column]
print(X)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(np.array(X[:, 0]), np.array(X[:, 1]))
plt.show()