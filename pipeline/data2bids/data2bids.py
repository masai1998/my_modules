"""
    transform dicom data to bids style
"""

import os, glob, string, tqdm, logging
import pandas as pd
from os.path import join as pjoin
from pipeline.utils.utils import bcolors, check_path, session_input_dict, session_task_dict, task_feature_dict, runcmd, heucreation, log_config, dict2json

def data2bids(args):

    # prepare logging
    log_config(pjoin(args.output_dir, 'data2bids.log'))

    # step 2 Information Reorganization
    print(bcolors.BOLD_NODE + "[Node] Re-organizing..." + bcolors.ENDC)
    # filter at first
    # traverse the scaninfo
    # generate session:input - determine
    # generate session:task
    # generate task:feature
    scaninfo_raw = pd.read_excel(args.scaninfo_file)
    # pandas:https://www.cnblogs.com/ech2o/p/11831488.html

    #
    if args.subject or args.session:
        scaninfo = scaninfo_raw
        if args.subject:
            logging.info('DATA2BIDS: Selected subject is {}'.format(args.subject))
            scaninfo = scaninfo[scaninfo['sub'].isin(args.subject)]
            scaninfo.reset_index(drop=True)
        if args.session:
            logging.info('DATA2BIDS: selected session is {}'.format(args.session))
            scaninfo = scaninfo[scaninfo['ses'].isin(args.session)]
            scaninfo.reset_index(drop=True)
        if args.quality_filter != 'all':
            logging.info('DATA2BIDS: quality filter is {}'.format(args.quality_filter))
            logging.info('DATA2BIDS: filtered scaninfo is in {}'.format(pjoin(args.output_dir, 'scaninfo_filtered.xlsx')))
            scaninfo = scaninfo[scaninfo['quality'] == args.quality_filter]
            scaninfo.reset_index(drop=True)
            scaninfo.to_excel(pjoin(args.output_dir, 'scaninfo_filtered.xlsx'))
    else:
        if args.quality_filter != 'all':
            logging.info('DATA2BIDS: quality filter is {}'.format(args.quality_filter))
            logging.info('DATA2BIDS: filtered scaninfo is stored in {}'.format(pjoin(args.output_dir, 'scaninfo_filtered.xlsx')))
            scaninfo = scaninfo_raw[scaninfo_raw['quality'] == args.quality_filter]
            scaninfo.reset_index(drop=True)
            scaninfo.to_excel(pjoin(args.output_dir, 'scaninfo_filtered.xlsx'))
        else:
            logging.info('DATA2BIDS: process all parts in {}'.format(args.scaninfo_file))
            scaninfo = scaninfo_raw

    # determine input of each session -- {sub-*/ses-* : *.tar.gz}
    session_input = session_input_dict(scaninfo)
    print("[news] Find {:d} session(s) waiting for processing..".format(len(session_input)))
    for key, value in session_input.items():
        print(bcolors.BOLD + "    {:s} ".format(key) + bcolors.ENDC + "from: {:s}".format(value))
    logging.info('DATA2BIDS: session-input mapping is stored in {}'.format(pjoin(args.output_dir, 'session-input.json')))
    dict2json(session_input, pjoin(args.output_dir, 'session-input.json'))


    # detemine session-contained tasks --
    session_task = session_task_dict(scaninfo)
    print("[news] Tasks in each sub-session collected")
    heu_session_task = {}
    for key, value in session_task.items():
        print(bcolors.BOLD + "    {:s} ".format(key) + bcolors.ENDC + "contains: {}".format(value))
        s_key = (key.split('-')[-1]).strip(string.digits)
        if s_key not in heu_session_task.keys():
            heu_session_task[s_key] = value
        else:
            if set(value) - set(heu_session_task[s_key]):
                heu_session_task[s_key].extend(list(set(value) - set(heu_session_task[s_key])))
    print("[news] Found {} kinds of session:".format(len(heu_session_task)))
    for key, value in heu_session_task.items():
        print(bcolors.BOLD + "    {:s} ".format(key) + bcolors.ENDC + "contains: {}".format(value))
    logging.info('DATA2BIDS: session-task mapping is stored in {}'.format(pjoin(args.output_dir, 'session-task.json')))
    dict2json(session_task, pjoin(args.output_dir, 'session-task.json'))

    # determine task feature -- task : [protocolname dim]
    task_feature = task_feature_dict(scaninfo)
    print("[news] Task feature information collected..")
    for key, value in task_feature.items():
        print(bcolors.BOLD + "    {:s} : ".format(key) + bcolors.ENDC + "protocolname = " + \
              bcolors.BOLD + "{0[0]},".format(value) + bcolors.ENDC + " dim = " + \
              bcolors.BOLD + "{0[1]} ".format(value) + bcolors.ENDC)
    logging.info('DATA2BIDS: task-feature mapping is stored in {}'.format(pjoin(args.output_dir, 'task-feature.json')))
    dict2json(task_feature, pjoin(args.output_dir, 'task-feature.json'))

    # step 3 Unpack
    print(bcolors.BOLD_NODE + "[Node] Unpacking..." + bcolors.ENDC)

    for _value in tqdm([__ for __ in session_input.values()]):
        # upack
        if not glob.glob(pjoin(args.temp_dir, _value.replace('.tar.gz', ''))):
            cmd = "tar -xzvf {:s} -C {:s}".format(pjoin(args.input_dir, _value), args.temp_dir)
            print("[news] Running command: {:s}".format(cmd))
            if not args.preview:
                runcmd(cmd)

    # step 4 Heuristic.py generation
    print(bcolors.BOLD_NODE + "[Node] Heuristic.py Generating..." + bcolors.ENDC)
    # task_feature & heu_session_task will be used
    for key, value in heu_session_task.items():
        check_path(pjoin(args.output_dir, 'code', key))
        file = pjoin(args.output_dir, 'code', key, 'heuristic.py')
        if not os.path.exists(file):
            heu_creation = heucreation(file)
            heu_creation.create_heuristic(value, task_feature)
    print("[news] Heuristic.py completion!")

    # step 5 heudiconv
    print(bcolors.BOLD_NODE + "[Node] BIDS converting..." + bcolors.ENDC)
    # session_input will be used
    for _key, _value in tqdm(session_input.items()):
        dicom_files = pjoin(args.temp_dir, _value).replace('.tar.gz', '/*.IMA')
        subID, sesID = _key.split('/')[0].replace('sub-', ''), _key.split('/')[1].replace('ses-', '')

        if not args.skip_feature_validation:
            # feature validation
            if args.overwrite:
                cmd = "heudiconv --files {:s} -o {:s} -f convertall -s {:s} -ss {:s} -c none --overwrite" \
                    .format(dicom_files, args.output_dir, subID, sesID)
            else:
                cmd = "heudiconv --files {:s} -o {:s} -f convertall -s {:s} -ss {:s} -c none" \
                    .format(dicom_files, args.output_dir, subID, sesID)
            print("[news] inspecting task feature in dicominfo.tsv")
            print("[news] command:" + bcolors.BOLD + " {}".format(cmd) + bcolors.ENDC)
            if not args.preview:
                runcmd(cmd)
                dicominfo = pd.read_csv("{:s}/.heudiconv/{:s}/info/dicominfo_ses-{:s}.tsv" \
                                        .format(args.output_dir, subID, sesID), sep='\t')
                dicominfo_scan_feature = list(
                    set([(dicominfo.iloc[_run, :]['protocol_name'], dicominfo.iloc[_run, :]['dim4']) \
                             if dicominfo.iloc[_run, :]['dim4'] != 1 else (
                        dicominfo.iloc[_run, :]['protocol_name'], dicominfo.iloc[_run, :]['dim3']) \
                         for _run in range(len(dicominfo))]))

                _check = []
                for _task in session_task[_key]:
                    _feature = (task_feature[_task][0], task_feature[_task][1])
                    if 'anat' in _task:
                        if not any([_feature[0] == __[0] for __ in dicominfo_scan_feature]):
                            _check.append(any([_feature[0] == __[0] for __ in dicominfo_scan_feature]))
                            logging.critical("'{:s}' protocol name mismtach! Found no {:s} in {:s}/.heudiconv/{:s}/info/dicominfo_ses-{:s}.tsv" \
                                             .format(_task, _feature[0], args.output_dir, subID, sesID))
                            print(bcolors.FAIL + \
                                  "[ERROR] '{:s}' protocol name mismtach! Found no {:s} in {:s}/.heudiconv/{:s}/info/dicominfo_ses-{:s}.tsv" \
                                  .format(_task, _feature[0], args.output_dir, subID, sesID) + bcolors.ENDC)
                    else:
                        if not _feature in dicominfo_scan_feature:
                            _check.append(_feature in dicominfo_scan_feature)
                            logging.critical("'{:s}' protocol name mismtach! Found no {:s} in {:s}/.heudiconv/{:s}/info/dicominfo_ses-{:s}.tsv" \
                                             .format(_task, _feature, args.output_dir, subID, sesID))
                            print(bcolors.FAIL + \
                                  "[ERROR] '{:s}' protocol name mismtach! Found no {:s} in {:s}/.heudiconv/{:s}/info/dicominfo_ses-{:s}.tsv" \
                                  .format(_task, _feature, args.output_dir, subID, sesID) + bcolors.ENDC)
                if not all(_check):
                    logging.critical('Feature validation failure!')
                    raise AssertionError(
                        '[ERROR] Feature validation failure! Please read [ERROR] message above or log for more details!')
                print(bcolors.BOLD + "[news] Feature validation seuccess!" + bcolors.ENDC)
                del _task, _feature

        heuristicpy = pjoin(args.output_dir, 'code', sesID.strip(string.digits), 'heuristic.py')
        if args.overwrite:
            cmd = "heudiconv --files {:s} -o {:s} -f {:s} -s {:s} -ss {:s} -c dcm2niix -b --overwrite" \
                .format(dicom_files, args.output_dir, heuristicpy, subID, sesID)
        else:
            cmd = "heudiconv --files {:s} -o {:s} -f {:s} -s {:s} -ss {:s} -c dcm2niix -b" \
                .format(dicom_files, args.output_dir, heuristicpy, subID, sesID)
        print("[news] Processing sub-{:s}/ses-{:s}".format(subID, sesID))
        print("    command: " + bcolors.BOLD + "{:s}".format(cmd) + bcolors.ENDC)
        if not args.preview:
            runcmd(cmd, timeout=3600)

    print('Log is saved in {}.'.format(pjoin(args.output_dir, 'data2bids.log')))

