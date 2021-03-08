"""
    run pipeline
"""

import argparse
from pipeline.data2bids.scripts import cnls_validation, data2bids

# initialize argparse
parser = argparse.ArgumentParser()

"""
    options
"""
parser.add_argument("--skip-cnls-validation", action="store_true", help="if choose, user can skip CNLS validation")
parser.add_argument("--data2bids", action="store_true", help="if choose, user can convert raw data to BIDS style")
parser.add_argument("--quality-filter", type=str, help="quality filter on scaninfo.xlsx", choices=['ok', 'all', 'discard'], default='ok')
parser.add_argument("--subject", type=str, nargs="+", help="subjects")
parser.add_argument("--session", type=str, nargs="+", help="sessions")
parser.add_argument("--preview", action="store_true", help="if choose, user can preview the whole pipeline and inspect critical information without runing any process command")
parser.add_argument("--skip-feature-validation", action="store_true", help="if choose, pipeline will not compare scan features between scaninfo.xlsx and dicom.tsv")
parser.add_argument("--overwrite", action="store_true", help="if choose, heudiconv will overwrite the existed files")

"""
    input and output
"""
parser.add_argument("--scaninfo", help="path to fetch scaninfo.xlsx")
parser.add_argument("--bold", help="base dir contains all relevant bold data, usually is /../bold", default=None)
parser.add_argument("--orig", help="input, defalut: orig", default='orig')
parser.add_argument("--dicom", help="temp folds for storage of decomposed data, default: orig/dicom", default='orig/dicom')
parser.add_argument("--nifti", help="name of directory stores nifti files with BIDS specifications, default: nifti", default='nifti')

args = parser.parse_args()

# cnls_validation
if not args.skip_cnls_validation:
    cnls_validation.cnls_validation(args)
# data2bids
if args.data2bids:
    data2bids.data2bids(args)










