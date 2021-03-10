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
    for path in [bold_dir, orig_dir, dicom_dir, nifti_dir]:
        check_path(path, mkdir)

    # Check if the orig_dir is empty
    if not os.listdir(orig_dir):
        logging.critical('orig_dir in {} is empty!'.format(orig_dir))
        raise AssertionError("[Critical] orig_dir in {} is empty!".format(orig_dir) + bcolors.ENDC)

        # if check_path(bold_dir, mkdir) == 0:
    #     logging.warning('{} is just created'.format(bold_dir))
    #     print("[Warning] {} is just created".format(bold_dir))
    # if check_path(bold_dir, mkdir) == 1:
    #     logging.warning('{} is not existed'.format(bold_dir))
    #     print("[Warning] {} is just created".format(bold_dir))
    # # orig
    # if check_path(orig_dir, mkdir) == 0:
    #     logging.warning('{} is just created'.format(orig_dir))
    #     print("[Warning] {} is just created".format(orig_dir))
    #
    # if bold_dir:
    #     os.chdir(bold_dir)
    #     # scaninfo
    #     if not os.path.exists(args.scaninfo):
    #         logging.critical('NOT FOUND {}'.format(args.scaninfo))
    #         raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(args.scaninfo) + bcolors.ENDC)
    #
    #     check_results = [check_path(_) for _ in [args.orig, args.dicom, args.nifti]]
    #     if check_results[0] == 0:
    #         logging.warning('{} is just created, it should be prepared before.'.format(args.orig))
    #         print("[Warning] {} is just created, it should be prepared before.".format(args.orig))
    #         if not os.listdir(args.orig):
    #             logging.critical('No files found in {}'.format(args.orig))
    #             raise AssertionError("No files found in {}".format(args.orig))
    #     if check_results[1] == 0:
    #         logging.warning('{} is just created, it should be prepared before.'.format(args.dicom))
    #         print("[Warning] {} is just created, it should be prepared before.".format(args.dicom))
    #     if check_results[2] == 0:
    #         logging.warning('{} is just created, it should be prepared before.'.format(args.nifti))
    #         print("[Warning] {} is just created, it should be prepared before.".format(args.nifti))
    #     if check_path(pjoin(args.orig, 'code')) == 0:
    #         logging.warning('{} is just created, it should be prepared before.'.format(pjoin(args.orig, 'code')))
    #         print("[Warning] {} is just created, it should be prepared before.".format(pjoin(args.orig, 'code')))
    #
    # else:
    #     if not os.path.exists(args.scaninfo):
    #         logging.critical("NOT FOUND {}".format(args.scaninfo))
    #         raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(args.scaninfo) + bcolors.ENDC)
    #     expect_folds = np.array([args.orig, args.dicom, args.nifti])
    #     absent_folds = expect_folds[np.array([check_path(_, 0) for _ in expect_folds])]
    #     if absent_folds:
    #         logging.critical("NOT FOUND {}".format(absent_folds))
    #         raise AssertionError(bcolors.FAIL + "[Error] NOT FOUND {}".format(absent_folds) + bcolors.ENDC)

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




