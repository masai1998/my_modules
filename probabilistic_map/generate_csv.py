import pandas as pd

subject_id = ['sub-M24','sub-M39','sub-M25','sub-M38','sub-M01','sub-M08','sub-M16','sub-M32','sub-M48','sub-M55','sub-M62','sub-M02','sub-M09','sub-M17','sub-M33','sub-M42','sub-M49','sub-M56','sub-M63','sub-M03','sub-M10','sub-M18','sub-M26','sub-M34','sub-M43','sub-M50','sub-M57','sub-M65','sub-M04','sub-M11','sub-M20','sub-M27','sub-M35','sub-M44','sub-M51','sub-M58','sub-M66','sub-M05','sub-M12','sub-M21','sub-M29','sub-M36','sub-M45','sub-M52','sub-M59','sub-M67','sub-M06','sub-M13','sub-M22','sub-M30','sub-M37','sub-M46','sub-M53','sub-M60','sub-M68','sub-M07','sub-M14','sub-M23','sub-M31','sub-M47','sub-M54','sub-M61']
task_id = ['Toe', 'Ankle', 'LeftLeg', 'RightLeg', 'Finger', 'Wrist', 'Forearm', 'Upperarm', 'Jaw', 'Lip', 'Tongue', 'Eye']

df1 = pd.DataFrame(subject_id)
df2 = pd.DataFrame(task_id)
df1.to_csv('subject_list.csv', header=None, index=None, columns=None)
df2.to_csv('task_list.csv', header=None, index=None, columns=None)