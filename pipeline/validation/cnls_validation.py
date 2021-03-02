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
    log_config(pjoin(args.base, 'info', 'CNLS_validation.log'))
    # step 1 Inspect directory
    print(bcolors.BOLD_NODE + "[Node] Inspecting..." + bcolors.ENDC)
    # inpect scaninfo.xlsx
    # expect using relative path, put in base -- /../bold
    # check input output & temp
    # inspect whether base match with BNL data orgniaztion specification
    # how about nifiti/code/

    # check
    if args.base:
        os.chdir(args.base)
        #
        if not os.path.exists(args.file):
            logging.critical('NOT FOUND {}'.format(args.file))
            raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(args.file) + bcolors.ENDC)
        #
        check_results = [check_path(_) for _ in [args.input_dir, args.temp_dir, args.output_dir]]
        if check_results[0] == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(args.input_dir))
            print("[Warning] {} is just created, it should be prepared before.".format(args.input_dir))
            if not os.listdir(args.input_dir):
                logging.critical('No files found in {}'.format(args.input_dir))
                raise AssertionError("No files found in {}".format(args.input_dir))
        if check_results[1] == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(args.temp_dir))
            print("[Warning] {} is just created, it should be prepared before.".format(args.temp_dir))
        if check_results[2] == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(args.output_dir))
            print("[Warning] {} is just created, it should be prepared before.".format(args.output_dir))
        if check_path(pjoin(args.input_dir, 'code')) == 0:
            logging.warning('{} is just created, it should be prepared before.'.format(pjoin(args.input_dir, 'code')))
            print("[Warning] {} is just created, it should be prepared before.".format(pjoin(args.input_dir, 'code')))

        #
        # expect_child = np.array(['info', 'nifti', 'orig'])
        # absent_child = expect_child[np.array([_ not in os.listdir(args.base) for _ in expect_child])]
        # if absent_child:
        #     print(bcolors.WARNING + "[Warning] data catalog structure mismatches with BNL specifications" \
        #           + bcolors.ENDC)
        #     print(bcolors.WARNING + "  NOTFOUND {0} absent in base path {1}".format(absent_child, args.base) \
        #           + bcolors.ENDC)
        #     print(bcolors.WARNING + "  It is encouraged to take use of CNLS specification, though not coerced..." \
        #           + bcolors.ENDC)
    else:
        if not os.path.exists(args.file):
            logging.critical("NOT FOUND {}".format(args.file))
            raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(args.file) + bcolors.ENDC)
        expect_folds = np.array([args.input_dir, args.temp_dir, args.output_dir])
        absent_folds = expect_folds[np.array([check_path(_, 0) for _ in expect_folds])]
        if absent_folds:
            logging.critical("NOT FOUND {}".format(absent_folds))
            raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(absent_folds) + bcolors.ENDC)

    print('Log is saved in {}.'.format(pjoin(args.base, 'info', 'CNLS_validation.log')))

