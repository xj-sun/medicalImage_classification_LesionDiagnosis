import os
import numpy as np 
import nibabel as nb
import pandas as pd 

data = pd.read_csv(csv_file) 
image = list(data['image'].values)
MEL = list(data['MEL'].values)
NV = list(data['NV'].values)
BCC = list(data['BCC'].values)
AKIEC = list(data['AKIEC'].values)
BKL = list(data['BKL'].values)
DF = list(data['DF'].values)
VASC = list(data['VASC'].values)

label_list = [MEL, NV, BCC, AKIEC, BKL, DF, VASC]
out_list = ['MEL', 'NV', 'BCC', 'AKIEC', 'BKL', 'DF', 'VASC']

count = 0
for img in os.listdir(image_dir):
    img_file = os.path.join(image_dir, img)
    for idx, image_name in enumerate(image):
        if image_name == img.split('.jpg')[0]:
            for idx_list, l_list in enumerate(label_list):
                if l_list[idx] == 1:
                    output_file = os.path.join(output_dir, out_list[idx_list], img)
                    os.system('mv \"{}\" \"{}\"'.format(img_file, output_file))
                    count += 1
                    print('[{}] moved {} to {}'.format(count, img, out_list[idx_list]))