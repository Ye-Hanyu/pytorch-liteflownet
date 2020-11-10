import cv2
import os
import numpy as np
import shutil
import models
import time
# from flow_vis import flow_vis
# from collections import Counter


video_path = '/home/rain/shipin/'
modeluse = 'kitti'  # 使用的训练模型
cut_path = '/home/rain/shipin/input/'  # 截取帧的位置
flo_path = '/home/rain/shipin/out/'  # 光流文件存储位置
png_out_path = '/home/rain/shipin/png_out/'  # 光流输出图片存储位置
length = 0  # 图像数量
mpthreshold = 20000  # 运动像素点阈值


# 提取视频帧
def videocut(video_path, cut_path):
    vidcap = cv2.VideoCapture(video_path + '厨房测试.mp4')  # 所提取视频名字
    success, image = vidcap.read()
    count = 0
    num = 0
    timeF = 24  # 截取间隔
    # success = True
    while success:
        success, image = vidcap.read()
        if(count % timeF == 0):
            if image is not None:  # 跳过某些视频最后一帧读取错误
                image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_AREA)
                # image = image[140:680, 200:1160]  # 需要保留的区域--裁剪
                # 参数1 是高度的范围，参数2是宽度的范围
                cv2.imwrite(cut_path + "/%d.png" %
                            num, image)   # 保存视频解帧图片
                num += 1
        count += 1
    vidcap.release()
# end


# 计算光流图
def flocalc():
    num = 0
    while (num + 1 < length):
        ml = 'python run.py\t' + '--model\t' + modeluse + '\t--first\t' \
            + cut_path + str(num) + '.png\t' + '--second\t' + cut_path + \
            str(num+1) + '.png\t' + '--out\t' + flo_path + str(num+1) + '.flo'
        os.system(ml)  # 命令行运行计算光流图
        num += 1
        """
        flo = np.load(flo_path + str(num+1) + '.flo',
                      encoding='bytes', allow_pickle=True)
        flopng = flow_vis.flow_to_color(flo, convert_to_bgr=False)
        cv2.imwrite(png_out_path + str(num) + '.png', flopng)
        print(str(num) + '.png' + ' done!')
        """
# end

# 计算光流图


def flo2png():
    num = 0
    while (num + 1 < length):
        kl = '~/pytorch-liteflownet/flow-code/color_flow\t' + flo_path + \
            str(num+1) + '.flo\t' + \
            png_out_path + str(num+1) + '.png'
        os.system(kl)  # 命令行运行光流图转PNG
        num += 1

# end

# 合成结果
def videomake(video_path, cut_path, png_out_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 合成视频编码
    videoWriter = cv2.VideoWriter(
        video_path + '/厨房测试结果2.avi', fourcc, 1, (640, 480))
    # 合成视频名称，编码，FPS，宽高
    timecount = 0
    for i in range(1, length):
        img1 = cv2.imread(cut_path + str(i) + '.png')
        img2 = cv2.imread(png_out_path + str(i) + '.png')
        lower = np.array([250, 250, 250])  # 过滤下限
        upper = np.array([256, 256, 256])  # 过滤下限
        mask = cv2.inRange(img2, lower, upper)  # 将指定颜色像素位置返回
        img2[mask != 0] = [0, 0, 0]  # 将指定像素颜色修改为黑色
        # 合并，其中参数1表示透明度，第一个1表示img1不透明，第二个1表示img2不透明
        img_mix = cv2.addWeighted(img1, 1, img2, 0.5, 0)

        x = models.detect(cut_path + str(i) + '.png')  # YOLO检测人
        person_num = 0  # 单帧出现的人数量
        status[i-1] = 0  # 是否有人的状态，0为没人
        

        for j in range(0, len(x)):  # 统计单帧人数量
            if (x[j][6] == 0):  # 检测目标是否为人
                person_num += 1
        if (person_num != 0):  # 有人的情况
            status[i-1] = 1
            timecount = 0
            print('People')
            cv2.putText(img_mix, 'Person!', (100, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        else:  # 无人的情况
            print('Nobody')
            cv2.putText(img_mix, 'No one!', (100, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
            timecount += 1
            if (timecount > 10):  # 无人多少帧后开始检测
                mp[i-1] = sum(sum(mask == 0))  # 计算图像中运动的像素点数量
                print(mp[i-1])
                count = 0
                if (i > 9):  # 检测连续图像中运动像素点数量是否大于阈值
                    for j in range(0, 9):
                        if (mp[i-1-j] > mpthreshold):  # 判断阈值
                            count += 1
                    if (count >= 8):  # 判断大于阈值的图像数量
                        cv2.putText(img_mix, 'Smoke!', (100, 200),
                                    cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
                # 在图像中加字
                        print('Smoke')
                    else:
                        cv2.putText(img_mix, 'Safe!', (100, 200),
                                    cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
                        print('safe')
        # img2g = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        # cv2.imwrite(png_out_path + "/gray%d.png" %
        #             i, img2g)
        # ms = sum(sum(img2g))
        # print(ms)
        # mp2 = sum(sum(img2g == 0))
        # print(mp2)

        videoWriter.write(img_mix)  # 将图片写入视频流
        print(str(i) + '.png' + ' done!')
    videoWriter.release()
# end


if __name__ == '__main__':
    # 清空文件夹
    time_start = time.time()
    shutil.rmtree(cut_path)
    os.mkdir(cut_path)
    shutil.rmtree(flo_path)
    os.mkdir(flo_path)
    shutil.rmtree(png_out_path)
    os.mkdir(png_out_path)
    # 代码运行开始
    videocut(video_path, cut_path)
    length = len(os.listdir(cut_path))
    mp = [0]*length
    status = [0]*length
    flocalc()
    flo2png()
    videomake(video_path, cut_path, png_out_path)
    time_end = time.time()
    print('Time cost:', time_end-time_start)
# end
