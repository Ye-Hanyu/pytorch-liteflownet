import cv2
import os
import numpy as np
# from PIL import Image

fourcc = cv2.VideoWriter_fourcc(*'XVID')
path1 = '/home/rain/shipin/input/'
path2 = '/home/rain/shipin/png_out/'
length = len(os.listdir(path2))

videoWriter = cv2.VideoWriter(
    '/home/rain/shipin/MVI_1983光流4.avi', fourcc, 8, (960, 540))
for i in range(1, length + 1):
    img1 = cv2.imread(path1 + str(i) + '.png')
    img2 = cv2.imread(path2 + str(i) + '.png')
    lower = np.array([250, 250, 250])
    upper = np.array([256, 256, 256])
    mask = cv2.inRange(img2, lower, upper)

    img_mask = np.copy(img2)
    img_mask[mask != 0] = [0, 0, 0]
    img2 = cv2.resize(img_mask, (960, 540))
    # cv2.imshow('img', img2)
    # cv2.waitKey(1)[']''0
    # 合并，其中参数1表示透明度，第一个1表示img1不透明，第二个1表示img2不透明
    # 如果改成0.5表示合并的时候已多少透明度覆盖。
    img_mix = cv2.addWeighted(img1, 1, img2, 0.6, 0)
    videoWriter.write(img_mix)
    print(str(i) + '.png' + ' done!')
videoWriter.release()
