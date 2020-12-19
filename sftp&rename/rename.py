"""
    rename.py
"""



import os

subjectlist = os.listdir(r'D:\deface')

for sub in subjectlist:
    print('processing ' + sub + '...')
    raw_file_name = os.listdir(os.path.join(r'D:\deface', sub))[0]
    new_file_name = raw_file_name.replace('_defaced', '',1)
    raw = os.path.join(r'D:\deface', sub, raw_file_name)
    new = os.path.join(r'D:\deface', sub, new_file_name)
    os.rename(raw, new)
    print('finish!')
