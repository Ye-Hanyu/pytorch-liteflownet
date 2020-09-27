import cv2
vidcap = cv2.VideoCapture('~/shipin/车离开.mp4')
success, image = vidcap.read()
count = 0
num = 0
timeF = 3
success = True
while success:
    success, image = vidcap.read()
    if(count % timeF == 0):
        # image = cv2.resize(image, (1280, 720), interpolation=cv2.INTER_AREA)
        # image = image[142:578, 128:1152]  # 需要保留的区域--裁剪
        # 参数1 是高度的范围，参数2是宽度的范围
        cv2.imwrite("~/shipin/input/%d.png" %
                    num, image)   # save frame as JPEG file
        num += 1
    count += 1
vidcap.release()
