"""
    run pipeline
"""

import argparse
from pipeline.validation import cnls_validation
from pipeline.data2bids import data2bids
from pipeline.preprocess import prepare_sdc, run_fmriprep, melodic_decompose

# argparse
parser = argparse.ArgumentParser()

# necessary parameters
parser.add_argument("file", help="path to fetch scaninfo.xlsx")
parser.add_argument("-b", "--base", help="base dir contains all relevant bold data, usually is /../bold", default=None)
parser.add_argument("-i", "--input-dir", help="input, defalut: orig", default='orig')
parser.add_argument("-t", "--temp-dir", help="temp folds for storage of decomposed data, default: orig/dcom", default='orig/dcom')
parser.add_argument("-o", "--output-dir", help="name of directory stores nifti files with BIDS specifications, default: nifti", default='nifti')

# optional parameters
parser.add_argument("-q", "--quality-filter", type=str, help="quality filter on scaninfo.xlsx", choices=['ok', 'all', 'discard'], default='ok')
parser.add_argument("-s", "--subject", type=str, nargs="+", help="subjects")
parser.add_argument("-ss", "--session", type=str, nargs="+", help="sessions")
parser.add_argument("-pr", "--preview", action="store_true", help="if choose, user can preview the whole pipeline and inspect critical information without runing any process command")
parser.add_argument("--skip-feature-validation", action="store_true", help="if choose, pipeline will not compare scan features between scaninfo.xlsx and dicom.tsv")
parser.add_argument("--overwrite", action="store_true", help="if choose, heudiconv will overwrite the existed files")

# customize pipeline
parser.add_argument("--skip-cnls-validation", action="store_true", help="")
parser.add_argument("--data2bids", action="store_true", help="")
parser.add_argument("--use-sdc", action="store_true", help="")
parser.add_argument("--fmriprep", action="store_true", help="")

args = parser.parse_args()

# cnls_validation
if not args.skip_cnls_validation:
    cnls_validation.cnls_validation(args)
# data2bids
if args.data2bids:
    data2bids.data2bids(args)
# fmriprep
# if args.use_sdc:






