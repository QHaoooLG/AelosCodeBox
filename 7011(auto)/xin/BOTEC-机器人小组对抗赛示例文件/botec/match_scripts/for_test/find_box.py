import time
import cv2
import threading
import numpy as np
import rospy
import math

from image_Tag_converter import ImgConverter

#定义一些参数
Head_img = None
HeadOrg = None

head_circle_x = None
head_circle_y = None
red_box_img_opened = None
red_box_img_closed = None
red_box_img_bgr = None
img2 = None

# 不同色块的hsv范围
color_range = {
    'red_box': [(156,43,46),(180,255,255)],
    'orange': [(16,139,86),(31,215,255)]
}

#获取图像
def get_img():
    global Head_img,HeadOrg
    global ret
    image_reader_chest = ImgConverter()
    while True:
        ret, HeadOrg = image_reader_chest.chest_image()
        time.sleep(1)
        if HeadOrg is not None:
            Head_img = HeadOrg
            time.sleep(0.05)
            #Head_img = cv2.flip(Head_img, 1)
        else:
            time.sleep(1)
            print("暂时未获取到图像")
th2 = threading.Thread(target=get_img)
th2.setDaemon(True)
th2.start()

#查找方块
def find_box(img,color_name):
    global head_circle_x, head_circle_y
    global red_box_img_opened,red_box_img_closed,red_box_img_bgr,img2
    if Head_img is None:
        print('等待获取图像中...')
        time.sleep(1)
    else:
        img2 = img
        red_box_img = img
        red_box_img_bgr = cv2.cvtColor(red_box_img, cv2.COLOR_RGB2BGR)  # 将图片转换到BRG空间
        red_box_img_hsv = cv2.cvtColor(red_box_img, cv2.COLOR_BGR2HSV)  # 将图片转换到HSV空间
        red_box_img = cv2.GaussianBlur(red_box_img_hsv, (3, 3), 0)  # 高斯模糊
        red_box_img_mask = cv2.inRange(red_box_img, color_range[color_name][0], color_range[color_name][1])  # 二值化
        red_box_img_closed = cv2.erode(red_box_img_mask, None, iterations=2)  # 腐蚀
        red_box_img_opened = cv2.dilate(red_box_img_mask, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算
        (contours, hierarchy) = cv2.findContours(red_box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            area = []
            for cn in contours:
                contour_area = math.fabs(cv2.contourArea(cn))
                area.append(contour_area)
            max_index = np.argmax(area)
            (head_circle_x, head_circle_y), head_radius = cv2.minEnclosingCircle(contours[max_index])
            cv2.circle(img, (int(head_circle_x), int(head_circle_y)), int(head_radius), (0, 0, 255))
            print('A','x=',head_circle_x,'y=',head_circle_y)
            cv2.imwrite('image.png', red_box_img_mask)
        else:
            print('正在寻找目标')

if __name__ == '__main__':
    rospy.init_node('image_listener')
    time.sleep(1)
    while True:
        while HeadOrg is None:
            print('wite')
            while True:
                find_box(Head_img, 'orange')