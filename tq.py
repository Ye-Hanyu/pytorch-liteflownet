import cv2
vidcap = cv2.VideoCapture('/home/rain/shipin/MVI_1981.MP4')
success, image = vidcap.read()
count = 0
num = 0
timeF = 3
success = True
while success:
    success, image = vidcap.read()
    if(count % timeF == 0):

        if image is not None:  
            # image = cv2.resize(image, (1280, 720), interpolation=cv2.INTER_AREA)
            image = image[540:1080, 500:1460]  # 需要保留的区域--裁剪
            # 参数1 是高度的范围，参数2是宽度的范围
            cv2.imwrite("/home/rain/shipin/input/%d.png" %
                    num, image)   # save frame as JPEG file
        num += 1
    count += 1
vidcap.release()
