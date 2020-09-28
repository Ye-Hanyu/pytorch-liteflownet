import cv2
import os

fourcc = cv2.VideoWriter_fourcc(*'XVID')
path = '/home/rain/shipin/png_out/'
length = len(os.listdir(path))

videoWriter = cv2.VideoWriter(
    '/home/rain/shipin/半烟fp=0.75.avi', fourcc, 10, (1920, 1080))
for i in range(1, length + 1):
    img = cv2.imread(path + str(i) + '.png')
    # cv2.imshow('img', img)
    # cv2.waitKey(1)[']''0
    videoWriter.write(img)
    print(str(i) + '.png' + ' done!')
videoWriter.release()
