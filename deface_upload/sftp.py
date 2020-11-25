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
    subjectlist = []
    temp_list = os.listdir(r'D:\MotorMapping_fixed_except_sub-retestM02')

    for file in temp_list:
        if 'sub-M' in file:
            subjectlist.append(file)
    #print(subjectlist)

    print('connecting...')
    sf = paramiko.Transport(host, port)
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    print('connection builded!')

    for subject in subjectlist:
        anatpath = r'/nfs/e4/function_guided_resection/MotorMapping/' + subject + r'/ses-01/anat'
        pwd_list = sftp.listdir(anatpath)
        for anatfile in pwd_list:
            if 'defaced' in anatfile:
                remote = anatpath + '/' + anatfile
                local = os.path.join('D:\deface', subject)
                if not os.path.exists(local):
                    os.makedirs(local)
                localpath = r'D:\\deface\\' + subject + r'\\' + anatfile
                print(remote)
                print(localpath)
                sftp.get(remote, localpath)
        print(subject + ' finish!')

    sf.close()
    print('connection closed.')