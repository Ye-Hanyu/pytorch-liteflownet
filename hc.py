import cv2
import os

fourcc = cv2.VideoWriter_fourcc(*'XVID')
path = '/home/rain/shipin/png_out/'
length = len(os.listdir(path))

videoWriter = cv2.VideoWriter(
    '/home/rain/shipin/test4.avi', fourcc, 10, (1280, 720))
for i in range(1, length + 1):  # 有多少张图片，从编号1到编号2629   
    img = cv2.imread(path + str(i) + '.png')
    # cv2.imshow('img', img)
    # cv2.waitKey(1)
    videoWriter.write(img)
    print(str(i) + '.png' + ' done!')
videoWriter.release()
