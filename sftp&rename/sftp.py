"""
    sftp.py
"""



import os
import paramiko

if __name__ == '__main__':
    host = '172.16.212.179'
    port = 22
    username = 'masai'
    password = 'ms4020665'

    subjectlist = ['sub-M01', 'sub-M02', 'sub-M03', 'sub-M04', 'sub-M05', 'sub-M06', 'sub-M07', 'sub-M08', 'sub-M09', 'sub-M10']
#    temp_list = os.listdir(r'D:\MotorMapping_fixed_except_sub-retestM02')
#    for file in temp_list:
#        if 'sub-M' in file:
#           subjectlist.append(file)
    #print(subjectlist)

    print('connecting...')
    sf = paramiko.Transport(host, port)
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    print('connection builded!')

    for subject in subjectlist:
        level2_results_dir = r'/nfs/e4/function_guided_resection/MotorMapping/derivatives/surface/ciftify/' + subject + r'/MNINonLinear/Results/ses-01_task-motor/ses-01_task-motor_hp200_s4_level2.feat/'
        #print(level2_results_dir)
        pwd_list = sftp.listdir(level2_results_dir)
        for result_file in pwd_list:
            if 'zstat_Head' in result_file:
                remote = os.path.join(level2_results_dir, result_file)
#                local = os.path.join('D:\level2_results\Head', subject)
#                if not os.path.exists(local):
#                    os.makedirs(local)
                localpath = os.path.join('/Users/masai/Documents/Head_zstat', result_file)
                # print(remote)
                # print(localpath)
                sftp.get(remote, localpath)
        print(subject + ' finish!')

    sf.close()
    print('connection closed.')