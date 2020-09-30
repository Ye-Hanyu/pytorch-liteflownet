import cv2
import os
import numpy as np
import shutil

video_path = '/home/rain/shipin/'
modeluse = 'kitti'  # 使用的训练模型
cut_path = '/home/rain/shipin/input/'  # 截取帧的位置
flo_path = '/home/rain/shipin/out/'  # 光流文件存储位置
png_out_path = '/home/rain/shipin/png_out/'  # 光流输出图片存储位置
length = 0


# 提取视频帧
def videocut(video_path, cut_path):
    vidcap = cv2.VideoCapture(video_path + 'MVI_1981.MP4')  # 所提取视频名字
    success, image = vidcap.read()
    count = 0
    num = 0
    timeF = 10  # 截取间隔
    # success = True
    while success:
        success, image = vidcap.read()
        if(count % timeF == 0):
            if image is not None:
                # image = cv2.resize(image, (1280, 720), interpolation=cv2.INTER_AREA)
                image = image[540:1080, 500:1460]  # 需要保留的区域--裁剪
                # 参数1 是高度的范围，参数2是宽度的范围
                cv2.imwrite(cut_path + "/%d.png" %
                            num, image)   # save frame as JPEG file
                num += 1
        count += 1
    
    # vidcap.release()

# 计算光流图


def flocalc(modeluse, cut_path, flo_path):
    num = 0
    while (num + 1 < length):
        ml = 'python run.py\t' + '--model\t' + modeluse + '\t--first\t' \
            + cut_path + str(num) + '.png\t' + '--second\t' + cut_path + \
            str(num+1) + '.png\t' + '--out\t' + flo_path + str(num+1) + '.flo'
        os.system(ml)
        kl = '~/pytorch-liteflownet/flow-code/color_flow\t' + flo_path + \
            str(num+1) + '.flo\t' + \
            png_out_path + str(num+1) + '.png'
        os.system(kl)
        num += 1

# 合成结果


def videomake(video_path, cut_path, png_out_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 合成视频编码

    videoWriter = cv2.VideoWriter(
        video_path + '/MVI_1982光流2.avi', fourcc, 3, (960, 540))  # 合成视频名称，编码，FPS，宽高
    for i in range(1, length):
        img1 = cv2.imread(cut_path + str(i) + '.png')
        img2 = cv2.imread(png_out_path + str(i) + '.png')
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
        img_mix = cv2.addWeighted(img1, 1, img2, 0.7, 0)
        videoWriter.write(img_mix)
        print(str(i) + '.png' + ' done!')
    videoWriter.release()


if __name__ == '__main__':
    shutil.rmtree(cut_path)
    os.mkdir(cut_path)
    shutil.rmtree(flo_path)
    os.mkdir(flo_path)
    shutil.rmtree(png_out_path)
    os.mkdir(png_out_path)
    videocut(video_path, cut_path)
    length = len(os.listdir(cut_path))
    flocalc(modeluse, cut_path, flo_path)
    videomake(video_path, cut_path, png_out_path)
