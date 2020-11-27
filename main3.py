import cv2
import os
import numpy as np
import models
import time
import torch
import serial
# from flow_vis import flow_vis
# from collections import Counter


modeluse = 'kitti'  # 使用的训练模型
width = 720
height = 480
mpthreshold = 100000  # 运动像素点阈值


def videocap():
    cap = cv2.VideoCapture("rtsp://admin:zhangxuexiang714@192.168.1.64/")  # 相机视频流
    # cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    img = cv2.resize(img, (width+200, height+200), interpolation=cv2.INTER_AREA)  # 修改尺寸
    img = img[100:580, 100:820]  # 需要保留的区域--裁剪
    # cv2.imwrite('./1.png', img)
    cap.release()
    return img
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


def frameDIFF(img1, img2):  # 帧间差分计算
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)  # 转灰度图
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    diff = cv2.absdiff(img1_gray, img2_gray)  #计算帧间差
    lower = np.array([1])  # 过滤下限
    upper = np.array([10])  # 过滤下限
    mask = cv2.inRange(diff, lower, upper)
    mp[0] = sum(sum(mask == 0))  # 计算图像中运动的像素点数量  # 将指定颜色像素位置返回
    diff[mask != 0] = [0]  # 将指定像素颜色修改为黑色
    IMG_OUT = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)  # 转彩色图
    IMG_OUT[:, :, 0] = 0  # 将蓝色通道置为0
    IMG_OUT[:, :, 1] = 0  # 将绿色通道置为0
    return IMG_OUT


if __name__ == '__main__':
    status = [0]
    mp = [0]
    count = 0
    scount = 0
    # dmesg | grep tty 查看端口
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)  # 端口设置
    print(ser)
    ser.close()
    ser.open()
    print(ser.isOpen())  # 端口状态打印
    while True:
        time_start = time.time()  # 开始计时
        imgcap1 = videocap()
        # time.sleep(0.5)
        imgcap2 = videocap()
        cv2.imwrite('./imgcap1.png', imgcap1)
        cv2.imwrite('./imgcap2.png', imgcap2)
        imgpredict = persondetect('./imgcap1.png')  # 检测人
        torch.cuda.empty_cache()  # cuda缓存清除
        cv2.imwrite('./imgpredict.png', imgpredict)
        co = co_detect()  # co浓度检测
        if (status[0] == 0):
            count += 1
        else:
            count = 0
        if (count >= 5):  # 烟雾检测延时，无人5帧后开始检测烟雾
            flowimg = frameDIFF(imgcap1, imgcap2)
            img_mix = cv2.addWeighted(imgcap1, 1, flowimg, 1, 0)  # 合成效果图
            print('Move Pixel:', mp)
            if (mp[0] > mpthreshold):
                cv2.putText(img_mix, 'Smoke!', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)  # 烟雾检测显示
            cv2.putText(img_mix, 'CO:%5.1f' % co, (50, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)  # co浓度显示
            cv2.imshow('1', img_mix)
            cv2.waitKey(20)

        else:
            cv2.putText(imgpredict, 'CO:%5.1f' % co, (50, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)
            cv2.imshow('1', imgpredict)
            cv2.waitKey(20)
        time_end = time.time()
        print('Time cost:', time_end-time_start)
# end
