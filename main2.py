import cv2
import os
import numpy as np
import shutil
import models
import time
import torch
import serial
# from flow_vis import flow_vis
# from collections import Counter


modeluse = 'kitti'  # 使用的训练模型
width = 720
height = 480
mpthreshold = 10000  # 运动像素点阈值


def videocap():
    cap = cv2.VideoCapture("rtsp://admin:zhangxuexiang714@192.168.1.64/")
    ret, img = cap.read()
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    # img = img[250:730, 600:1320]  # 需要保留的区域--裁剪
    # cv2.imwrite('./1.png', img)
    cap.release()
    return img
# end


# 提取视频帧
def videocut():
    vidcap = cv2.VideoCapture(video_path + inputvideo)  # 所提取视频名字
    success, image = vidcap.read()
    count = 0
    num = 0
    timeF = 6  # 截取间隔
    # success = True
    while success:
        success, image = vidcap.read()
        if(count % timeF == 0):
            if image is not None:  # 跳过某些视频最后一帧读取错误
                image = cv2.resize(image, (720, 480), interpolation=cv2.INTER_AREA)
                # image = image[140:680, 200:1160]  # 需要保留的区域--裁剪
                # 参数1 是高度的范围，参数2是宽度的范围
                cv2.imwrite(cut_path + "/%d.png" %
                            num, image)   # 保存视频解帧图片
                num += 1
        count += 1
    vidcap.release()
# end


# 计算光流图
def flocalc(img1, img2):
    ml = 'python run.py ' + '--model ' + modeluse + ' --first ' + img1 +\
         ' --second ' + img2 + ' --out ' + './flow.flo'
    os.system(ml)  # 命令行运行计算光流图
# end


def flo2png(flo):
    kl = '~/pytorch-liteflownet/flow-code/color_flow\t' + flo + '\t' + './flow.png'
    os.system(kl)  # 命令行运行光流图转PNG
# end


def delwhite(img):
    lower = np.array([250, 250, 250])  # 过滤下限
    upper = np.array([256, 256, 256])  # 过滤下限
    mask = cv2.inRange(img, lower, upper)
    mp[0] = sum(sum(mask == 0))  # 计算图像中运动的像素点数量  # 将指定颜色像素位置返回
    img[mask != 0] = [0, 0, 0]  # 将指定像素颜色修改为黑色
    return img
# end


# 合成结果
def videomake(img):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 合成视频编码
    videoWriter = cv2.VideoWriter(
        video_path + './厨房测试结果.avi', fourcc, 4, (720, 480))
    # 合成视频名称，编码，FPS，宽高           
        #     print('People')
        #     cv2.putText(img_mix, 'Person!', (100, 100),
        #                 cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        # else:  # 无人的情况
        #     print('Nobody')
        #     cv2.putText(img_mix, 'No one!', (100, 100),
        #                 cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        #     timecount += 1
        #     if (timecount > 10):  # 无人多少帧后开始检测
        #         mp[i-1] = sum(sum(mask == 0))  # 计算图像中运动的像素点数量
        #         print(mp[i-1])
        #         count = 0
        #         if (i > 9):  # 检测连续图像中运动像素点数量是否大于阈值
        #             for j in range(0, 9):
        #                 if (mp[i-1-j] > mpthreshold):  # 判断阈值
        #                     count += 1
        #             if (count >= 8):  # 判断大于阈值的图像数量
        #                 cv2.putText(img_mix, 'Smoke!', (100, 200),
        #                             cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        #         # 在图像中加字
        #                 print('Smoke')
        #             else:
        #                 cv2.putText(img_mix, 'Safe!', (100, 200),
        #                             cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        #                 print('safe')
        # img2g = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        # cv2.imwrite(png_out_path + "/gray%d.png" %
        #             i, img2g)
        # ms = sum(sum(img2g))
        # print(ms)
        # mp2 = sum(sum(img2g == 0))
        # print(mp2)

        # videoWriter.write(img_mix)  # 将图片写入视频流
        # print(str(i) + '.png' + ' done!')
    videoWriter.release()
# end


def persondetect(img):
    x = models.detect(img)  # YOLO检测人
    person_num = 0  # 单帧出现的人数量
    # status = list  # 是否有人的状态，0为没人
    img = cv2.imread(img)
    for j in range(0, len(x)):  # 统计单帧人数量
        if ((x[j][6] == 0) and (x[j][4] > 0.6)):  # 检测目标是否为人
            person_num += 1
            x1 = int(x[j][0] * width)
            y1 = int(x[j][1] * height)
            x2 = int(x[j][2] * width)
            y2 = int(x[j][3] * height)
            rgb = (0, 0, 255)
            img = cv2.rectangle(img, (x1, y1), (x2, y2), rgb, 2)
    if (person_num != 0):  # 有人的情况
        status[0] = 1
    else:
        status[0] = 0
    return img


def co_detect():
    hex_str = bytes.fromhex('01 03 00 12 00 01 24 0F')
    ser.write(hex_str)
    res = ser.readall()
    temp = res.hex()
    print("16进制源数据:", temp)
    d1 = temp[6:10]
    d1 = int(d1, 16)
    d1 = float(d1)/10
    print("10进制数据是:", d1)
    return d1


if __name__ == '__main__':
    status = [0]
    mp = [0]
    count = 0
    scount = 0
    # dmesg | grep tty 查看端口
    # ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
    # print(ser)
    # ser.close()
    # ser.open()
    # print(ser.isOpen())
    while True:
        time_start = time.time()
        imgcap1 = videocap()
        # time.sleep(0.5)
        imgcap2 = videocap()
        cv2.imwrite('./imgcap1.png', imgcap1)
        cv2.imwrite('./imgcap2.png', imgcap2)
        imgpredict = persondetect('./imgcap1.png')
        torch.cuda.empty_cache()
        cv2.imwrite('./imgpredict.png', imgpredict)
        # co = co_detect()
        if (status[0] == 0):
            count += 1
        else:
            count = 0
            scount = 0
        if (count >= 1):
            flocalc('./imgcap1.png', './imgcap2.png')
            flo2png('./flow.flo')
            flowimg = cv2.imread('./flow.png')
            flowimg = delwhite(flowimg)
            img_mix = cv2.addWeighted(imgcap1, 1, flowimg, 0.5, 0)
            scount += 1
            if (scount > 1):
                print('Move Pixel:', mp)
                if (mp[0] > mpthreshold):
                    cv2.putText(img_mix, 'Smoke!', (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)
            # cv2.putText(img_mix, 'CO:%5.1f' % co, (50, 450),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)
            cv2.imshow('1', img_mix)
            cv2.waitKey(20)

        else:
            # cv2.putText(imgpredict, 'CO:%5.1f' % co, (50, 450),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)
            cv2.imshow('1', imgpredict)
            cv2.waitKey(20)
        time_end = time.time()
        print('Time cost:', time_end-time_start)
# end
