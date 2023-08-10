import os
import numpy as np
import scipy.io as sio
from random import sample
import SimpleITK as sitk
from scipy import stats
import csv

task = 1
patch_size = 25
margin = int(np.floor((patch_size - 1) / 2.0))
input_shape = (patch_size, patch_size, patch_size)

# x_prop = range(15, 166, 25)
# y_prop = range(20, 209, 25)
# print(list(y_prop))

# load data.mat
data = sio.loadmat('data.mat')

sample_name = data['samples_train'].flatten()
labels = data['labels_train'].flatten()

#image path
path = ''

#5 fold
for i in range(5):
    # 20% training samples as the validation set
    valid_list = range(len(sample_name) // 5 * i, len(sample_name) // 5 * (i + 1))
    train_list = list(set(range(len(sample_name))).difference(set(valid_list)))
    samples_train = sample_name[train_list]
    pos = [path + sub for sub in samples_train if sub.split('/')[-2] == 'AD']
    neg = [path + sub for sub in samples_train if sub.split('/')[-2] == 'NC']
    print(len(pos))
    print(len(neg))
    mincount = min(len(pos), len(neg))

    pvalue_list = []
    inputs_coor = []
    pos_inputs = []
    neg_inputs = []

    #num_patches = 7 * 8 * 7
    for p in range(7 * 8 * 7):
        pvalue_list.append('n')
        inputs_coor.append('n')
        pos_inputs.append(np.zeros(mincount, dtype='float32'))

        neg_inputs.append(np.zeros(mincount, dtype='float32'))

    # calculated patch location proposals on training samples
    # template_cors = 'template_center_fold{}_size{}.mat'.format(i + 1, patch_size)
    cnt = 0
    for x_i in range(15, 166, 25):
        for y_i in range(20, 209, 25):
            for z_i in range(15, 166, 25):
                print('x,y,z:{},{},{}'.format(x_i, y_i, z_i))
                for iteration, img_pos in enumerate(pos[:mincount]):
                    I_pos = sitk.ReadImage(img_pos.strip())
                    img = np.array(sitk.GetArrayFromImage(I_pos))
                    pos_img_patch = np.mean(img[x_i - margin: x_i + margin + 1,
                                            y_i - margin: y_i + margin + 1,
                                            z_i - margin: z_i + margin + 1])
                    print('iter', iteration)
                    pos_inputs[cnt][iteration] = pos_img_patch

                for iteration, img_neg in enumerate(neg[:mincount]):
                    I_neg = sitk.ReadImage(img_neg.strip())
                    img = np.array(sitk.GetArrayFromImage(I_neg))
                    neg_img_patch = np.mean(img[x_i - margin: x_i + margin + 1,
                                            y_i - margin: y_i + margin + 1,
                                            z_i - margin: z_i + margin + 1])
                    print('iter', iteration)
                    neg_inputs[cnt][iteration] = neg_img_patch

                inputs_coor[cnt] = '{}.{}.{}'.format(x_i, y_i, z_i)

                cnt = cnt + 1
    
    #t-test
    for pi in range(cnt):
        levene = stats.levene(neg_inputs[pi], pos_inputs[pi])
        if levene.pvalue > 0.05:
            s = True
        else:
            s = False

        t, p = stats.ttest_ind(neg_inputs[pi], pos_inputs[pi], nan_policy='omit', equal_var=s)
        print(p)
        if np.isnan(p):
            p = 1

        pvalue_list[pi] = '{}'.format(p)

    print(pvalue_list)
    with open('patch_loc_fold_{}.csv'.format(i), 'w') as file1:
        writer = csv.writer(file1)
        writer.writerow(inputs_coor)
        writer.writerow(pvalue_list)


