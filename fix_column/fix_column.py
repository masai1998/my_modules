"""
    fix_column.py
"""

import os
import pandas as pd

def get_subname(path):
    list_sub = []
    list_temp_sub = os.listdir(path)
    for foldername in list_temp_sub:
        if 'sub-M' in foldername:
            list_sub.append(foldername)
    return list_sub

def get_tsv_path(path):
    # get tsv name
    list_tsv_path = []
    list_sub = get_subname(path)
    for sub in list_sub:
        path_func = path + '/' + sub + r'/ses-01/func'
        list_temp_tsv = os.listdir(path_func)
        for filename in list_temp_tsv:
            if '.tsv' in filename:
                tsv_path = os.path.join(path_func , filename)
                list_tsv_path.append(tsv_path)
    return list_tsv_path

def exchange_column_trial_type_duration(data_inpath,data_outpath):
    list_tsv_path = get_tsv_path(data_inpath)
    for tsv_path in list_tsv_path:
        current_tsv_data = pd.read_csv(tsv_path , sep='\t')
        temp = list(current_tsv_data)
        temp.insert(1, temp.pop(temp.index('duration')))
        current_tsv_data = current_tsv_data.loc[:, temp]
        #print(tsv_path)
        tsv_folder_name = tsv_path[43:50]
        #print(tsv_folder_name)
        tsv_name = tsv_path[43:]
        #print(tsv_name)
        save_path = os.path.join(data_outpath , tsv_folder_name , 'ses-01' , 'func' , tsv_name)
        current_tsv_data = pd.DataFrame(current_tsv_data)
        current_tsv_data.to_csv(save_path , sep='\t' , index=False)



data_inpath = r'D:/MotorMapping_source'
data_outpath = r'D:\MotorMapping_1_change_duration_column'
exchange_column_trial_type_duration(data_inpath,data_outpath)
