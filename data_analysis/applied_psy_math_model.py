"""
    appiled_psy_math_model.py
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def data_analysis(data_file):

    # read data

    data = pd.read_excel(data_file, usecols=[0, 2, 3, 4])
    data.columns = ['group_id', 'y', 'x1', 'x2']
    # print(data)

    # prepare x and y

    x = sm.add_constant(data.iloc[:, 2:])
    y = data['y']

    # compute model

    model = sm.OLS(y, x)
    result = model.fit()
    print(result.summary())

















if __name__ == '__main__':
    data_file = 'D:\Group_data_analysisi.xlsx'
    data_analysis(data_file)





