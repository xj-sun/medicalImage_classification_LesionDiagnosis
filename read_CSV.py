import os
import numpy as np 
import nibabel as nb
import pandas as pd 

txt_file = ''
data_dir = ''


csv_file = ''


data = pd.read_csv(csv_file) 
MRN = list(data['MRN'].values)
DOB = list(data['DOB'].values)

data2 = pd.read_csv(csv_file2) 
CPT_MRN = list(data2['MRN'].values)
CPT_DATE = list(data2['CPT_DATE'].values)

data3 = pd.read_csv(csv_file3) 
ICD_MRN = list(data3['MRN'].values)
ICD_DATE = list(data3['ICD_DATE'].values)

MRN2AGE_ICD = {}
MRN2AGE_CPT = {}
for idx, m in enumerate(MRN):
    if m not in MRN2AGE_CPT:
        DOB_m = DOB[idx]

        CPT_date_m_idx = CPT_MRN.index(m)
        CPT_date_m = CPT_DATE[CPT_date_m_idx]

        ICD_date_m_idx = ICD_MRN.index(m)
        ICD_date_m = CPT_DATE[ICD_date_m_idx]

        year_ICD = int(ICD_date_m.split('/')[-1])
        year_CPT = int(CPT_date_m.split('/')[-1])
        year_DOB = int(DOB_m.split('/')[-1])

        MRN2AGE_ICD[m] = year_ICD-year_DOB
        MRN2AGE_CPT[m] = year_CPT-year_DOB



normal_cases_CPT = []
for item in MRN2AGE_CPT:
    if MRN2AGE_CPT[item] < 50 and MRN2AGE_CPT[item] >= 18:
        normal_cases_CPT.append(item)

normal_cases_ICD = []
for item in MRN2AGE_ICD:
    if MRN2AGE_ICD[item] < 50 and MRN2AGE_ICD[item] >= 18:
        normal_cases_ICD.append(item)




lookup_table_A = ''
lookup_table_B = ''

with open(lookup_table_A) as f:
    content = f.readlines()
content_A = [x.strip() for x in content]

with open(lookup_table_B) as f:
    content = f.readlines()
content_B = [x.strip() for x in content]


MRN2TUMA_B = {}
for item in content_B:
    MRN_code = item.split('/')[1].split('=')[0]
    TUMA_code = item.split('/')[1].split('=')[1]
    MRN2TUMA_B[MRN_code] = TUMA_code

MRN2TUMA_A = {}
for item in content_A:
    MRN_code = item.split('/')[1].split('=')[0]
    TUMA_code = item.split('/')[1].split('=')[1]
    MRN2TUMA_A[MRN_code] = TUMA_code


count = 0
selected_MRN2DOB_A = {}
for item in MRN2TUMA_A:
    MRN_code = int(item)
    if MRN_code in MRN:
        idx = MRN.index(MRN_code)
        selected_MRN2DOB_A[item] = DOB[idx]
        count += 1


count = 0
selected_MRN2DOB_B = {}
for item in MRN2TUMA_B:
    MRN_code = int(item)
    if MRN_code in MRN:
        idx = MRN.index(MRN_code)
        selected_MRN2DOB_B[item] = DOB[idx]
        count += 1


TUMA2DOB_A = {}
for item in selected_MRN2DOB_A:
    TUMA2DOB_A[MRN2TUMA_A[item]] = selected_MRN2DOB_A[item]

TUMA2DOB_B = {}
for item in selected_MRN2DOB_B:
    TUMA2DOB_B[MRN2TUMA_B[item]] = selected_MRN2DOB_B[item]


tuma2DOB_file = os.path.join(output_dir, 'TUMA2DOB_B.txt')
wr_file = open(tuma2DOB_file, 'w')

for item in TUMA2DOB_B:
    wr_file.write(item + ' ' + TUMA2DOB_B[item] + '\n')
wr_file.close()



date_txt_A = ''

TUMA2DATE_A = {}

with open(date_txt_A) as f:
    content = f.readlines()
content_A_date = [x.strip() for x in content]

for item in content_A_date:
    items = item.split(' ')
    tuma_code = items[0]
    date = items[3]
    TUMA2DATE_A[tuma_code] = date

date_txt_B = ''


TUMA2DATE_B = {}

with open(date_txt_B) as f:
    content = f.readlines()
content_B_date = [x.strip() for x in content]

for item in content_B_date:
    items = item.split(' ')
    tuma_code = items[0]
    date = items[3]
    TUMA2DATE_B[tuma_code] = date



TUMA2AGE_A = {}
for item in TUMA2DATE_A:
    scan_date = TUMA2DATE_A[item]
    DOB = TUMA2DOB_A[item]
    DOB_year = int(DOB.split('/')[-1])
    scan_year = int(int(scan_date) / 10000)
    TUMA2AGE_A[item] = scan_year - DOB_year

TUMA2AGE_B = {}
for item in TUMA2DATE_B:
    scan_date = TUMA2DATE_B[item]
    DOB = TUMA2DOB_B[item]
    DOB_year = int(DOB.split('/')[-1])
    scan_year = int(int(scan_date) / 10000)
    TUMA2AGE_B[item] = scan_year - DOB_year

tuma2DOB_file = os.path.join(output_dir, 'TUMA2AGE_B.txt')
wr_file = open(tuma2DOB_file, 'w')

for item in TUMA2AGE_B:
    wr_file.write(item + ' ' + str(TUMA2AGE_B[item]) + '\n')
wr_file.close()



age_A = []
for item in TUMA2AGE_A:
    if TUMA2AGE_A[item] > 21 and TUMA2AGE_A[item] <= 40:
        age_A.append(item)

age_B = []
for item in TUMA2AGE_B:
    if TUMA2AGE_B[item] > 21 and TUMA2AGE_B[item] <= 40:
        age_B.append(item)



# copy subjects
count = 0
for subject in age_B:
    for image in os.listdir(image_B_dir):
        if subject in image:
            image_file = os.path.join(image_B_dir, image)
            out_file = os.path.join(output_dir, image)
            os.system('cp \"{}\" \"{}\"'.format(image_file, out_file))
            count += 1
            print('[{}] copied {}'.format(count, image))


# make new spreadshhet for de-id demo and ICD codes

data = pd.read_csv(csv_file) 
MRN = list(data['MRN'].values)
SEX = list(data['SEX'].values)
RACE = list(data['RACE'].values)
ETHNICITY = list(data['ETHNICITY'].values)
DOB = list(data['DOB'].values)
WEIGHT = list(data['WEIGHT'].values)
HEIGHT = list(data['HEIGHT'].values)
BMI = list(data['BMI'].values)

# data2 = pd.read_csv(csv_file2) 
# CPT_MRN = list(data2['MRN'].values)
# CPT_DATE = list(data2['CPT_DATE'].values)

data3 = pd.read_csv(csv_file3) 
ICD_MRN = list(data3['MRN'].values)
ICD_DESCRIPTION = list(data3['ICD_DESCRIPTION'].values)

ICD_code = list(data3['ICD_CODE'].values)

mergeICD = {}

for idx, item in enumerate(ICD_MRN):
    if item not in mergeICD:
        mergeICD[item] = []
    mergeICD[item].append(ICD_code[idx])







A_file = os.path.join(output_dir, 'De_id_spreadsheep_A.txt')
wr_file = open(A_file, 'w')
wr_file.write('De_id SEX RACE ETHNICITY AGE WEIGHT HEIGHT BMI ICD' + '\n')

for item in MRN:
    item_str = str(item)
    if item_str in MRN2TUMA_A:
        MRN_idx = MRN.index(item)
        TUMA_code = MRN2TUMA_A[item_str]
        # TUMA_id = TUMA_code.split('_')[1]
        if TUMA_code not in TUMA2AGE_A:
            age = 'none'
        else:
            age = TUMA2AGE_A[TUMA_code]
        # ICD_idx = ICD_MRN.index(item)
        ICD_list = str(mergeICD[item])
        ICD_list = ICD_list.split('[')[1].split(']')[0]
        wr_file.write(TUMA_code + '/' + str(SEX[MRN_idx]) +  '/' + str(RACE[MRN_idx]) + '/' + str(ETHNICITY[MRN_idx]) + \
            '/' + str(age) + '/' + str(WEIGHT[MRN_idx]) + '/' + str(HEIGHT[MRN_idx]) + '/' + str(BMI[MRN_idx]) + '/' + str(ICD_list) + '\n')
wr_file.close()


# save descrition2codes

data3 = pd.read_csv(csv_file3) 
ICD_MRN = list(data3['MRN'].values)
ICD_DESCRIPTION = list(data3['ICD_DESCRIPTION'].values)

ICD_code = list(data3['ICD_CODE'].values)

code2des = {}

for idx, item in enumerate(ICD_code):
    if item not in code2des:
        code2des[item] = ICD_DESCRIPTION[idx]



A_file = os.path.join(output_dir, 'code2descrition.txt')
wr_file = open(A_file, 'w')

for item in code2des:
    wr_file.write(item + ':' + code2des[item] + '\n')
wr_file.close()



#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# read image MRN2ICD

data = pd.read_csv(csv_file) 
ICD_MRN = list(data['MRN'].values)

ICD_DESCRIPTION = list(data['ICD_DESCRIPTION'].values)
ICD_DATE = list(data['ICD_DATE'].values)

ICD_code = list(data['ICD_CODE'].values)
ICD_type = list(data['ICD_TYPE'].values)


MRN2ICD_code = {}

for idx, item in enumerate(ICD_MRN):
    item_MRN = item
    item_date = ICD_DATE[idx]
    item_ICD_code = ICD_code[idx]
    item_type = ICD_TYPE[idx]