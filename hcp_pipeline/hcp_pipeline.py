"""
    hcp_pipeline.py
"""



import fmriprep
import ciftify
import task_analysis




class hcp_pipeline(object):

    def __init__(self, data_input_path, fmriprep_output_path, fmriprep_workdir, ciftify_workdir, fsf_template_path, subject_list_path, task_list_path):
        self.data_input_path = data_input_path
        self.fmriprep_output_path = fmriprep_output_path
        self.fmriprep_workdir = fmriprep_workdir
        self.ciftify_workdir = ciftify_workdir
        self.fsf_template_path = fsf_template_path
        self.subject_list_path = subject_list_path
        self.task_list_path = task_list_path

    def run_hcp_pipeline(self):
        fmriprep.run_fmriprep(self)
        ciftify.run_ciftify(self)
        task_analysis.run_all_level_analysis(self)



if __name__ == '__main__':


