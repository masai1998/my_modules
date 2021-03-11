"""
    validation before data2bids
"""

import os, argparse, logging
from os.path import join as pjoin

class bcolors:
    WARNING = '\033[33m'
    FAIL = '\033[41m'
    BOLD_NODE = '\033[1;32m'
    BOLD = '\033[1;34m'
    ENDC = '\033[0m'

def log_config(log_name):
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.INFO, filename=log_name, filemode='w')

def check_path(path, mkdir):
    if type(path) == str:
        if not os.path.exists(path):
            if mkdir:
                os.mkdir(path)
                logging.warning('{} does not exist but validator has been created automatically.'.format(path))
                print('[Warning] {} does not exist but validator has been created automatically.'.format(path))
            else:
                logging.warning('{} does not exist.'.format(path))
                print("[Warning] {} does not exist.".format(path))
        else:
            logging.info('{} already exists.'.format(path))
            print("[info] {} already exists.".format(path))
    else:
        raise AssertionError("Input must be str")

def cnls_validation(args):

    print(bcolors.BOLD_NODE + "[Node] Checking..." + bcolors.ENDC)

    # prepare required path and parameter
    bold_dir = pjoin(args.projectdir, 'data', 'bold')
    orig_dir = pjoin(args.projectdir, 'data', 'bold', 'orig')
    dicom_dir = pjoin(args.projectdir, 'data', 'bold', 'dicom')
    nifti_dir = pjoin(args.projectdir, 'data', 'bold', 'nifti')
    info_dir = pjoin(args.projectdir, 'data', 'bold', 'info')
    derivatives_dir = pjoin(args.projectdir, 'data', 'bold', 'derivatives')
    if args.create:
        mkdir = 1
    else:
        mkdir = 0

    # prepare logging
    log_config(pjoin(bold_dir, 'info', 'CNLS_validation.log'))

    # Check if the file/folder exists
    if not os.path.exists(args.scaninfo):
        logging.critical('scaninfo file in {} is not found!'.format(args.scaninfo))
        raise AssertionError(bcolors.FAIL + "[Critical] NOT FOUND {}".format(args.scaninfo) + bcolors.ENDC)
    for path in [bold_dir, orig_dir, dicom_dir, nifti_dir, info_dir, derivatives_dir]:
        check_path(path, mkdir)

    # Check if the orig_dir is empty
    if not os.listdir(orig_dir):
        logging.critical('orig_dir in {} is empty!'.format(orig_dir))
        raise AssertionError("[Critical] orig_dir in {} is empty!".format(orig_dir) + bcolors.ENDC)

    print('Log is saved in {}.'.format(pjoin(bold_dir, 'info', 'CNLS_validation.log')))

if __name__ == '__main__':

    # initialize argparse
    parser = argparse.ArgumentParser()

    """
       required parameters 
    """
    parser.add_argument("scaninfo", help="path to fetch scaninfo.xlsx")
    parser.add_argument("projectdir", help="base dir contains all project files")

    """
        optinal parameters 
    """
    parser.add_argument("--create", action="store_true", help="if choose, validator will create required folder if it is not exist.")

    args = parser.parse_args()

    # CNLS validation
    cnls_validation(args)




