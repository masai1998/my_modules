"""
    validation before data2bids
"""

import os
import logging
import numpy as np
from os.path import join as pjoin
from pipeline.utils.utils import bcolors, check_path, log_config

def cnls_validation(args):

    # prepare logging
    log_config(pjoin(args.bold, 'info', 'CNLS_validation.log'))
    # step 1 Inspect directory
    print(bcolors.BOLD_NODE + "[Node] Inspecting..." + bcolors.ENDC)
    # inpect scaninfo.xlsx
    # expect using relative path, put in base -- /../bold
    # check input output & temp
    # inspect whether base match with BNL data orgniaztion specification
    # how about nifiti/code/

    # check
    if args.bold:
        os.chdir(args.bold)
        #
        if not os.path.exists(args.scaninfo):
            logging.critical('NOT FOUND {}'.format(args.scaninfo))
            raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(args.scaninfo) + bcolors.ENDC)
        #
        check_results = [check_path(_) for _ in [args.orig, args.dicom, args.nifti]]
        if check_results[0] == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(args.orig))
            print("[Warning] {} is just created, it should be prepared before.".format(args.orig))
            if not os.listdir(args.orig):
                logging.critical('No files found in {}'.format(args.orig))
                raise AssertionError("No files found in {}".format(args.orig))
        if check_results[1] == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(args.dicom))
            print("[Warning] {} is just created, it should be prepared before.".format(args.dicom))
        if check_results[2] == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(args.nifti))
            print("[Warning] {} is just created, it should be prepared before.".format(args.nifti))
        if check_path(pjoin(args.orig, 'code')) == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(pjoin(args.orig, 'code')))
            print("[Warning] {} is just created, it should be prepared before.".format(pjoin(args.orig, 'code')))

        #
        # expect_child = np.array(['info', 'nifti', 'orig'])
        # absent_child = expect_child[np.array([_ not in os.listdir(args.bold) for _ in expect_child])]
        # if absent_child:
        #     print(bcolors.WARNING + "[Warning] data catalog structure mismatches with BNL specifications" \
        #           + bcolors.ENDC)
        #     print(bcolors.WARNING + "  NOTFOUND {0} absent in base path {1}".format(absent_child, args.bold) \
        #           + bcolors.ENDC)
        #     print(bcolors.WARNING + "  It is encouraged to take use of CNLS specification, though not coerced..." \
        #           + bcolors.ENDC)
    else:
        if not os.path.exists(args.scaninfo):
            logging.critical("NOT FOUND {}".format(args.scaninfo))
            raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(args.scaninfo) + bcolors.ENDC)
        expect_folds = np.array([args.orig, args.dicom, args.nifti])
        absent_folds = expect_folds[np.array([check_path(_, 0) for _ in expect_folds])]
        if absent_folds:
            logging.critical("NOT FOUND {}".format(absent_folds))
            raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(absent_folds) + bcolors.ENDC)

    print('Log is saved in {}.'.format(pjoin(args.bold, 'info', 'CNLS_validation.log')))

