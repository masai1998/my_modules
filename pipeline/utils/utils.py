"""
    utlis.py
        bcolors(class):

"""

import os, glob, argparse, string, json
import subprocess
import pandas as pd
import numpy as np
from os.path import join as pjoin
from tqdm import tqdm
import logging

# ====================================
# class
# ====================================

class bcolors:
    WARNING = '\033[33m'
    FAIL = '\033[41m'
    BOLD_NODE = '\033[1;32m'
    BOLD = '\033[1;34m'
    ENDC = '\033[0m'

class heucreation:
    """
    this class will automatically create the heuritics.py
    """

    def __init__(self, file):
        self.file = open(file, 'a+')
        self.HEADER = [
            'import os\ndef create_key(template, outtype=(\'nii.gz\',), annotation_classes=None):\n    if template is None or not template:\n        raise ValueError(\'Template must be a valid format string\')\n    return template, outtype, annotation_classes\ndef infotodict(seqinfo):\n    """Heuristic evaluator for determining which runs belong where\n    allowed template fields - follow python string module:\n    item: index within category\n    subject: participant id\n    seqitem: run number during scanning\n    subindex: sub index within group\n    """\n\n']

    def write_catalog(self, task_list):
        """
        write catalog rules part
        parameters:
        -----------
        task_list : list, value of session_task dict, like ['func_rest', 'fmap/magnitude']
        """
        content = []
        for _ in task_list:
            mod, label = _.split('/')[0], _.split('/')[1]
            if mod in ['anat', 'dwi', 'fmap']:
                content.append(
                    "    {0}_{1} = create_key('sub-{{subject}}/{{session}}/{0}/sub-{{subject}}_{{session}}_run-{{item:02d}}_{1}')\n" \
                    .format(mod, label))
            if mod in ['func']:
                content.append(
                    "    {0}_{1} = create_key('sub-{{subject}}/{{session}}/{0}/sub-{{subject}}_{{session}}_task-{1}_run-{{item:02d}}_bold')\n" \
                    .format(mod, label))
        self.file.writelines(content)

    def write_info(self, task_list):
        """
        write the info dict part
        parameters:
        -----------
        task_list: list, value of session_task dict, like ['func_rest', 'fmap/magnitude']
        """

        content = ["\n    info = {"] + ["{0[0]}_{0[1]}:[],".format(_.split('/')) for _ in task_list[:-1]] \
                  + ["{0[0]}_{0[1]}:[]}}\n".format(_.split('/')) for _ in [task_list[-1]]]

        self.file.writelines(content)

    def write_condition(self, task_list, feature_dict):
        """
        write the condition part
        parameters:
        ----------
        task_list: list
        feaure_dict: dict
        """
        openning = ["\n    for idx, s in enumerate(seqinfo):\n"]
        ending = ["    return info\n"]
        middle = []
        for _ in task_list:
            mod, label = _.split('/')[0], _.split('/')[1]
            if mod == 'anat':
                middle.append("        if ('{}' in s.protocol_name):\n".format(feature_dict[_][0]))
                middle.append("            info[{0}_{1}].append(s.series_id)\n".format(mod, label))
            if mod == 'fmap':
                middle.append(
                    "        if ('{0[0]}' in s.protocol_name) and (s.dim3 == {0[1]}):\n".format(feature_dict[_]))
                middle.append("            info[{0}_{1}].append(s.series_id)\n".format(mod, label))
            if mod == 'func':
                middle.append(
                    "        if ('{0[0]}' in s.protocol_name) and (s.dim4 == {0[1]}):\n".format(feature_dict[_]))
                middle.append("            info[{0}_{1}].append(s.series_id)\n".format(mod, label))
        content = openning + middle + ending
        self.file.writelines(content)

    def create_heuristic(self, task_list, feature_dict):
        """
        create the heuristic.py according to task_list & feature_dict
        parameters:
        -----------
        task_list: list
        feature_dict: dict
        """
        self.file.writelines(self.HEADER)
        self.write_catalog(task_list)
        self.write_info(task_list)
        self.write_condition(task_list, feature_dict)
        self.file.close()

# ====================================
# functions
# ====================================

def runcmd(command, verbose=0, timeout=1200):
    """
    run command line
    """
    ret = subprocess.run(command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding="utf-8", timeout=timeout)
    if ret.returncode == 0 and verbose:
        print("success:", ret)
    elif ret.returncode != 0:
        print("error:", ret)


def check_path(path, mk=1):
    if type(path) == str:
        if not os.path.exists(path):
            if mk:
                os.mkdir(path)
                print("[news] Inspected: {} created.".format(path))
            else:
                print("[news] Inspected: {} not existed.".format(path))
            return 0
        else:
            print("[news] Inspected: {} have exsited".format(path))
            return 1
    else:
        raise AssertionError("Input must be str")


def session_input_dict(scaninfo):
    """
    Generate a dict show where the data of each session from.
    parameter:
    ----------
    scaninfo:pd.DataFrame

    return:
    ---------
    session_input: dict
    """
    session_input = {}
    print("[news] Generating session-input mapping...")
    for _ in tqdm(range(len(scaninfo))):
        cur_run = scaninfo.iloc[_, :]
        _key = "sub-{:02d}/ses-{:s}".format(cur_run['sub'], cur_run['ses'])
        if _key not in session_input.keys():
            session_input[_key] = "{0}*{1}.tar.gz".format(cur_run['date'].strftime("%Y%m%d"), cur_run['name'])

    return session_input


def session_task_dict(scaninfo):
    """
    Generate a dict show where the data of each session from.
    Won't contain fmap/ cause every session should have one
    parameter:
    ----------
    scaninfo锛?pd.DataFrame

    return:
    ---------
    session_task: dict
    """
    session_task = {}
    print("[news] Generating session-task mapping...")
    for _ in tqdm(range(len(scaninfo))):
        cur_run = scaninfo.iloc[_, :]
        for __ in cur_run['ses'].split(','):
            _key = "sub-{:02d}/ses-{:s}".format(cur_run['sub'], __)
            if _key not in session_task.keys():
                session_task[_key] = ["{:s}/{:s}".format(cur_run['modality'], cur_run['task'])]
            else:
                value = "{:s}/{:s}".format(cur_run['modality'], cur_run['task'])
                if not value in session_task[_key]:
                    session_task[_key].append("{:s}/{:s}".format(cur_run['modality'], cur_run['task']))
    return session_task


def task_feature_dict(scaninfo):
    """
    Generate a dict ponit out feature of each task
    parameter:
    ----------
    scaninfo: pd.DataFrame

    return
    -------------
    task_feature: dict
    """
    task_feature = {}
    print("[news] Generating task-feature mapping...")
    for _ in tqdm(range(len(scaninfo))):
        cur_run = scaninfo.iloc[_, :]
        _key = "{:s}/{:s}".format(cur_run['modality'], cur_run['task'])
        if _key not in task_feature.keys():
            if not np.isnan(cur_run['dim']):
                task_feature[_key] = [cur_run['protocol_name'], int(cur_run['dim'])]
            else:
                task_feature[_key] = [cur_run['protocol_name'], None]
    return task_feature

def log_config(log_name):
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.INFO, filename=log_name, filemode='w')

def dict2json(dict, path):
    dict = json.dumps(dict)
    with open(path, "w+", encoding='utf-8') as f:
        f.write(dict + ",\n")


