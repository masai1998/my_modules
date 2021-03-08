"""
    fill fmap json files
"""

import os
from os.path import join as pjoin
import json

def fill_json(args):
    # baisc infomation about dataset
    bids_fold = args.nifti
    # subjects = ['core{:02d}'.format(i+1) for i in range(10)]
    subjects = [args.subject]

    # ===========================

    # %% []
    # load fold info
    sessions = {name: [] for name in (subjects)}  # {sub : [session]}
    jsonfiles = {name: {sesname: [] for sesname in sessions[name]} for name in (subjects)}  # {sub:{session:[files]}}
    intendedfornii = {name: {sesname: [] for sesname in sessions[name]} for name in
                      (subjects)}  # {sub:{session:[files]}}

    # collect .json files waiting to fill & .nii.gz filenames
    for subname in sessions.keys():
        # get all the sessions under a subject
        subpth = pjoin(bids_fold, 'sub-%s' % (subname))
        sessions[subname] = os.listdir(subpth)
        # collect jsonfiles & values
        for fold in sessions[subname]:
            # path preparation
            sesspth = pjoin(bids_fold, subpth, fold)
            fmappth = pjoin(sesspth, 'fmap')
            funcpth = pjoin(sesspth, 'func')
            # if fmap exist then clollect
            if os.path.exists(fmappth):
                jsonfiles[subname][fold] = [file for file in os.listdir(fmappth) if '.json' in file]
                # the file path must be the relative path to sub- folder
                intendedfornii[subname][fold] = ['%s/func/%s' % (fold, file) for file in os.listdir(funcpth) if
                                                 '.nii.gz' in file]

    # write key:value for each json
    for sub, ses_fold in jsonfiles.items():
        for ses, files in ses_fold.items():
            for file in files:
                # file path
                file_path = pjoin(bids_fold, 'sub-%s/%s' % (sub, ses), 'fmap', file)

                # load in & add IntendedFor
                with open(file_path, 'r') as datafile:
                    data = json.load(datafile)
                data['IntendedFor'] = intendedfornii[sub][ses]

                # save out
                with open(file_path, 'w') as datafile:
                    json.dump(data, datafile)
        print('%s done' % sub)



