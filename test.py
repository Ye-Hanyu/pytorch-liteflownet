import cv2
import numpy as np

mp = 0
img1 = cv2.imread('./33.png')
img2 = cv2.imread('./34.png')
img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
diff = cv2.absdiff(img1_gray, img2_gray)
lower = np.array([1])  # 过滤下限
upper = np.array([5])  # 过滤下限
mask = cv2.inRange(diff, lower, upper)
mp = sum(sum(mask == 0))  # 计算图像中运动的像素点数量  # 将指定颜色像素位置返回
diff[mask != 0] = [0]  # 将指定像素颜色修改为黑色
IMG_OUT = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
IMG_OUT[:, :, 0] = 0
IMG_OUT[:, :, 1] = 0
cv2.imshow('1', IMG_OUT)
cv2.waitKey()
