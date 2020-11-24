"""
    third level test
"""



import os
import subprocess

# prepare fMRI names and fsf names

subject_list = ['sub-M24', 'sub-M25', 'sub-M26', 'sub-M27', 'sub-M29',]
for subject in subject_list:
    level1_tasks = '@'.join(subject_list)
    level1_fsfs = level1_tasks
    level2_tasks = 'ses-01_task-motor'
    level2_fsf = level2_tasks

# input parameters

subject = 'sub-M24-25-26-27-29'
resultsFolder = '/nfs/e2/workingshop/masai/test/hcp_pipeline/ciftify/sub-M24-25-26-27-29/MNINonLinear/Results/'
downSampleFolder = '/nfs/e2/workingshop/masai/test/hcp_pipeline/ciftify/sub-M24-25-26-27-29/MNINonLinear/fsaverage_LR32k/'
levelOnefMRINames = level1_tasks
levelOnefsfNames = level1_fsfs
levelTwofMRIName = level2_tasks
levelTwofsfName = level2_fsf
lowResMesh = '32'
finalSmoothingFWHM = '4'
temporalFilter = '200'
volumeBasedProcessing = 'No'
regName = 'NONE'
parcellation = 'NONE'

# process third level analysis

analysis_command = ' '.join(['${HCPPIPEDIR}/TaskfMRIAnalysis/scripts/TaskfMRIAnalysis.sh',
                            #Subject
                            subject,
                            #ResultsFolder
                            resultsFolder,
                            #DownSampleFolder
                            downSampleFolder,
                            #LevelOnefMRINames
                            levelOnefMRINames,
                            #LevelOnefsfNames
                            levelOnefsfNames,
                            #LevelTwofMRIName
                            levelTwofsfName,
                            #LevelTwofsfName
                            levelTwofMRIName,
                            #LowResMesh
                            lowResMesh,
                            #FinalSmoothingFWHM
                            finalSmoothingFWHM,
                            #TemporalFilter
                            temporalFilter,
                            #VolumeBasedProcessing
                            volumeBasedProcessing,
                            #RegName
                            regName,
                            #Parcellation
                            parcellation])
subprocess.check_call(analysis_command, shell=True)

