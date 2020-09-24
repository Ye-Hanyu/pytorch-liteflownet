import cv2
vidcap = cv2.VideoCapture('/home/rain/shipin/2.mov')
success, image = vidcap.read()
count = 0
num = 0
timeF = 1
success = True
while success:
    success, image = vidcap.read()
    if(count % timeF == 0):
        # image = image[142:578,128:1152] #需要保留的区域--裁剪
        # 参数1 是高度的范围，参数2是宽度的范围
        cv2.imwrite("/home/rain/shipin/input/%d.png" %
                    num, image)   # save frame as JPEG file
        num += 1
    count += 1
vidcap.release()
