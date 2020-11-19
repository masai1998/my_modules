"""
    run_pipeline.py
"""



import generate_results_list
import generate_probabilistic_map



if __name__ == '__main__':
    cifti_path = '/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify'
    subject_list_path = '/nfs/s2/userhome/masai/workingdir/subject_list.csv'
    second_level_feat_folder_path = 'MNINonLinear/Results/ses-01_task-motor/ses-01_task-motor_hp200_s4_level2.feat'
    generate_results_list.results_list_pipeline(cifti_path, subject_list_path, second_level_feat_folder_path)

    task_list_path = '/nfs/s2/userhome/masai/workingdir/task_list.csv'
    results_list_path = '/nfs/s2/userhome/masai/workingdir/results_list.csv'
    z_threshold_value = 3
    participants_number = 62
    generate_probabilistic_map.probabilistic_map_pipeline(task_list_path, results_list_path, z_threshold_value, participants_number)