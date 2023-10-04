import time
import cv2
import threading
import numpy as np
import math
# from image_converter import ImgConverter

color_range = {
    'red_box' : [(156,43,46),(180,255,255)],
    'orange': [(12 , 51 , 136), (18 , 210 , 225)]
}

Head_img = None    #宽480 高640
ret = False
pi=math.pi

cap_head = cv2.VideoCapture(0)   #选择读取哪个摄像头

#获取图像
def get_img():
    global Head_img
    global ret
    # image_reader_head = ImgConverter()
    while True:

        if cap_head.isOpened():
            ret,HeadOrg = cap_head.read()
        # ret, HeadOrg = image_reader_head.head_image()
        if HeadOrg is not None:
            Head_img = HeadOrg
            time.sleep(0.05)
            #Head_img = cv2.flip(Head_img, 1)
        else:
            time.sleep(1)
            print("暂时未获取到图像")

th1 = threading.Thread(target=get_img)
th1.setDaemon(True)
th1.start()

#查找红色方块
def find_red_box(img,color_name):
    if Head_img is None:
        time.sleep(1)
    else:
        red_box_img = img
        red_box_img_bgr = cv2.cvtColor(red_box_img, cv2.COLOR_RGB2BGR)  # 将图片转换到BRG空间
        red_box_img_hsv = cv2.cvtColor(red_box_img, cv2.COLOR_BGR2HSV)  # 将图片转换到HSV空间
        red_box_img = cv2.GaussianBlur(red_box_img_hsv, (3, 3), 0)  # 高斯模糊
        red_box_img_mask = cv2.inRange(red_box_img, color_range[color_name][0], color_range[color_name][1])  # 二值化
        red_box_img_closed = cv2.erode(red_box_img_mask, None, iterations=2)  # 腐蚀
        red_box_img_opened = cv2.dilate(red_box_img_closed, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算

        # cv2.imshow('P',red_box_img_opened)
        # cv2.waitKey(10)
        (contours, hierarchy) = cv2.findContours(red_box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            area = []
            for cn in contours:
                contour_area = math.fabs(cv2.contourArea(cn))
                area.append(contour_area)
            max_index = np.argmax(area)
            (head_circle_x, head_circle_y), head_radius = cv2.minEnclosingCircle(contours[max_index])
            cv2.circle(img,(int(head_circle_x), int(head_circle_y)),int(head_radius),(0,0,255))
        else:
            print('wite')
        # print('x值',head_circle_x,'y值', head_circle_y)
        cv2.imshow('img',img)
        cv2.waitKey(10)

if __name__ == '__main__' :
    while True:
        find_red_box(Head_img,'orange')
        time.sleep(0.05)