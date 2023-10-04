# encoding:utf-8
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import platform
import argparse
import time
import threading

"""
功能:读取一张图片,显示出来,转化为HSV色彩空间
     并通过滑块调节HSV阈值,实时显示
"""

printNote = ("左键图片选择颜色, 右键清除范围, 窗口按q打印结果 \n erode 溶蚀量, dilate 膨胀量")

# 请修改文件路径
# 本地文件位置
imagePath = 'img/004.jpg'
# 网页图片位置,本地图片不存在时会打开网页图片
imageURL = 'http://192.168.8.169:8080/stream_viewer?topic=/usb_cam_chest/image_raw'

FATCH_RATE = 0.5


FLAG_URL = False
FLAG_GET_PARSE = True

image = None

mouse_hsv = None
mouse_flag = 0
lowerbH = 0
lowerbS = 0
lowerbV = 0
upperbH = 0
upperbS = 0
upperbV = 0

plt_h = []
plt_s = []
plt_v = []
max_record = [0, 0, 0]
min_record = [255, 255, 255]


def fetchImageFromHttp(caper, timeout_s=1):
    try:
        success, frame = caper.read()
        if success:
            return frame
        else:
            return []
    except Exception as error:
        print('获取图片失败', error)
        return []


def nothing(x):
    pass


def hsv_max(aa, bb):
    cc = [bb[0], bb[1], bb[2]]
    if aa[0] > bb[0]:
        cc[0] = aa[0]
    if aa[1] > bb[1]:
        cc[1] = aa[1]
    if aa[2] > bb[2]:
        cc[2] = aa[2]
    return cc


def hsv_min(aa, bb):
    cc = [bb[0], bb[1], bb[2]]
    if aa[0] < bb[0]:
        cc[0] = aa[0]
    if aa[1] < bb[1]:
        cc[1] = aa[1]
    if aa[2] < bb[2]:
        cc[2] = aa[2]
    return cc


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 定义一个鼠标左键按下去的事件
        global mouse_flag, mouse_hsv, lowerbH, lowerbS, lowerbV, upperbH, upperbS, upperbV, image
        global max_record, min_record

        # 窗口清理，保证动态刷新数值
        system = platform.system()
        if (system == u'Windows'):
            os.system('cls')
        else:
            os.system('clear')

        # 获取鼠标点击区域
        dst = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # BGR转HSV
        mouse_hsv = dst[y, x]

        plt_h.append(mouse_hsv[0])
        plt_s.append(mouse_hsv[1])
        plt_v.append(mouse_hsv[2])
        max_record = hsv_max(mouse_hsv, max_record)
        min_record = hsv_min(mouse_hsv, min_record)

        # 打印鼠标选择的图像HSV信息
        print("鼠标选中区域值为: ", min_record, " ", max_record)

        print("滑动条HSV范围是: ")
        print("(", lowerbH, ',', lowerbS, ',', lowerbV,
              "),(", upperbH, ',', upperbS, ',', upperbV, ')')

        print(printNote)

        mouse_flag = 1
    if event == cv2.EVENT_RBUTTONDOWN:
        # 窗口清理，保证动态刷新数值
        system = platform.system()
        if (system == u'Windows'):
            os.system('cls')
        else:
            os.system('clear')

        max_record = [0, 0, 0]
        min_record = [255, 255, 255]

        # 打印鼠标选择的图像HSV信息
        print("鼠标选中区域值已清除")

        print("滑动条HSV范围是: ")
        print("(", lowerbH, ',', lowerbS, ',', lowerbV,
              "),(", upperbH, ',', upperbS, ',', upperbV, ')')

        print(printNote)

        mouse_flag = 0


def fetchURL():
    global image, FATCH_RATE
    image_url = imageURL.replace("stream_viewer","stream")
    cap = cv2.VideoCapture(image_url)
    while True:
        image = fetchImageFromHttp(cap)
        time.sleep(FATCH_RATE)

def fetchOnceURL():
    image_url = imageURL.replace("stream_viewer","stream")
    cap = cv2.VideoCapture(image_url)
    success, frame = cap.read()
    if success:
        return frame
    else:
        print("无法获取图像")
        return success

def main():
    global mouse_flag, mouse_hsv, lowerbH, lowerbS, lowerbV, upperbH, upperbS, upperbV
    global min_record, max_record, image
    global FLAG_GET_PARSE, FLAG_URL

    winName = "Quit with \'q\'"
    # winName = winName.decode('utf-8')
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winName, 800, 1000)

    if FLAG_GET_PARSE and FLAG_URL:
        image = fetchOnceURL()
    elif FLAG_GET_PARSE and FLAG_URL == False:
        image = cv2.imread(imagePath)
    if FLAG_GET_PARSE == False:
        image = cv2.imread(imagePath)  # 根据路径读取一张图片
        if image is None:
            image = fetchOnceURL()
            FLAG_URL = True
            if image is None:
                print("请填写正确的文件路径")
                exit()
    cv2.imshow(winName, image)
    cv2.setMouseCallback(winName, mouse_click)

    print(printNote)
    # 可以自己设定初始值，最大值255不需要调节
    cv2.createTrackbar('LowerbH', winName, 0, 180, nothing)
    cv2.createTrackbar('UpperbH', winName, 180, 180, nothing)
    cv2.createTrackbar('LowerbS', winName, 0, 255, nothing)
    cv2.createTrackbar('UpperbS', winName, 255, 255, nothing)
    cv2.createTrackbar('LowerbV', winName, 0, 255, nothing)
    cv2.createTrackbar('UpperbV', winName, 255, 255, nothing)

    cv2.createTrackbar('erode', winName, 0, 50, nothing)
    cv2.createTrackbar("dilate", winName, 0, 50, nothing)

    if FLAG_URL:
        urlImagefetch_thread = threading.Thread(target=fetchURL, daemon=True)
        urlImagefetch_thread.start()

    while True:
        lowerbH = cv2.getTrackbarPos('LowerbH', winName)
        upperbH = cv2.getTrackbarPos('UpperbH', winName)
        lowerbS = cv2.getTrackbarPos('LowerbS', winName)
        upperbS = cv2.getTrackbarPos('UpperbS', winName)
        lowerbV = cv2.getTrackbarPos('LowerbV', winName)
        upperbV = cv2.getTrackbarPos('UpperbV', winName)

        erodeValue = cv2.getTrackbarPos('erode', winName)
        dilateValue = cv2.getTrackbarPos('dilate', winName)

        dst = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # BGR转HSV
        dst = cv2.inRange(dst, (lowerbH, lowerbS, lowerbV),
                          (upperbH, upperbS, upperbV))  # 通过HSV的高低阈值，提取图像部分区域

        dst = cv2.erode(dst, np.ones((erodeValue, erodeValue), dtype=np.uint8))
        dst = cv2.dilate(dst, np.ones(
            (dilateValue, dilateValue), dtype=np.int8))
        # 输入图像与输入图像在掩模条件下按位与，得到掩模范围内的原图像
        img_specifiedColor = cv2.bitwise_and(image, image, mask=dst)

        if mouse_flag:
            mouse_hsv_str = 'H:'+"%d" %min_record[0] + '~'+ "%d" %max_record[0] + ' S:'+"%d" %(min_record[
                1]) + '~'+"%d" %(max_record[1]) + ' V:'+"%d" %(min_record[2]) + '~'+"%d" %(max_record[2])

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img_specifiedColor, mouse_hsv_str,
                        (50, 50), font, 0.8, (0, 0, 0), 5)
            cv2.putText(img_specifiedColor, mouse_hsv_str,
                        (50, 50), font, 0.8, (255, 255, 255), 2)

        cv2.imshow(winName, img_specifiedColor)
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("关闭并打印结果")
            print("[(", lowerbH, ',', lowerbS, ',', lowerbV,
                  "),(", upperbH, ',', upperbS, ',', upperbV, ')]')
            print("erode:",erodeValue,' dilate:',dilateValue)
            break
    cv2.destroyAllWindows()


def parse_args():
    description = "-"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--img", type=str, default=None,help="输入图片地址 如:img/004.jpg")
    parser.add_argument("-u","--url", type=str, default=None, help="从网页串流获取 如:http://192.168.8.168:8080/stream_viewer?topic=/usb_cam_chest/image_raw")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(args.img,args.url)
    if args.url is not None:
        imageURL = args.url
        FLAG_URL = True
    elif args.img is not None:
        imagePath = args.img
    else:
        FLAG_GET_PARSE = False

    main()
