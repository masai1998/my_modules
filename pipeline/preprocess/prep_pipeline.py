"""

"""

import argparse
from pipeline.preprocess.scripts import prepare_sdc, run_fmriprep, melodic_decompose

# initialize argparse
parser = argparse.ArgumentParser()

"""
    options
"""
parser.add_argument("--fmriprep", action="store_true", help="")
parser.add_argument("--melodic-decompose", action="store_true", help="")
parser.add_argument("--subject", type=str, nargs="+", help="subjects")
"""
    input and output
"""
parser.add_argument("--nifti", help="name of directory stores nifti files with BIDS specifications")
parser.add_argument("--fmriprep-output", help="name of directory stores preprocessed files")
parser.add_argument("--fmriprep-workdir", help="name of directory stores temp files")
parser.add_argument("--ica-output", help="name of directory stores melodic decomposed files")


args = parser.parse_args()

# fmriprep
if args.fmriprep:
    prepare_sdc.fill_json(args)
    run_fmriprep.run_fmriprep(args)

# melodic
if args.melodic_decompose:
    melodic_decompose.melodic_decompose(args)
