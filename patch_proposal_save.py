import os
import csv
import shutil

import numpy as np
import SimpleITK as sitk
from scipy import ndimage
import scipy.io as sio

fold = 4
patch_num = 60
patch_size = 25
sourcepath = 'patch_loc_fold_{}.csv'.format(fold)

trainxy = np.loadtxt(sourcepath, delimiter=',', dtype=np.str_, skiprows=1)

x_cors = []
y_cors = []
z_cors = []
coors = np.zeros((3, patch_num))

len = trainxy.shape[0]
print(len)
for i, id in enumerate(trainxy[:patch_num, 0]):
    print(i)
    coors[0, i] = int(id.split('.')[0])
    coors[1, i] = int(id.split('.')[1])
    coors[2, i] = int(id.split('.')[2])


sio.savemat('template_center_fold{}_size{}.mat'.format(fold+1, patch_size), {'patch_centers': coors})
