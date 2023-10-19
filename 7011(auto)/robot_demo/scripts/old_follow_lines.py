#!/usr/bin/env python3
# coding:utf-8

import numpy as np
import cv2
import math
import serial
import threading
import time
import datetime
import rospy
import CMDcontrol
import tf
from math import sqrt
from geometry_msgs.msg import PoseWithCovarianceStamped
from ar_track_alvar_msgs.msg import AlvarMarkers
from ar_track_alvar_msgs.msg import AlvarMarker
from kickBallOnly import kick_ball
# from startDoorOnly import start_door
from image_converter import ImgConverter
from color_filter import color_filter

chest_r_width = 480
chest_r_height = 640
img_debug = True

action_DEBUG = False
CMDcontrol = None

chest_ret = True    
ChestOrg_img = None  

color_range = {
               'yellow_door': [(24 , 151 , 95), (30 , 183 , 122)],
               'black_door': [(0 , 11 , 19), (165 , 132 , 35)],
               'black_gap': [(0, 0, 0), (180, 255, 70)],
               'yellow_hole': [(20, 120, 95), (30, 250, 190)],
               'black_hole': [(5, 80, 20), (40, 255, 100)],
               'chest_red_floor': [(0, 40, 60), (20,200, 190)],
               'chest_red_floor1': [(0, 100, 60), (20,200, 210)],
               'chest_red_floor2': [(110, 100, 60), (180,200, 210)],
                'green_bridge': [(50, 75, 70), (80, 240, 210)],
               }

def thread_move_action():
    CMDcontrol.CMD_transfer()


def action(act_name):
    print(f'执行动作: {act_name}')
    time.sleep(1)   
    CMDcontrol.action_append(act_name)  # 调用CMDcontrol.py中的函数在动作队列中添加动作


def init_action_thread():   # 初始化动作线程
    th3 = threading.Thread(target=thread_move_action)
    th3.setDaemon(True)
    th3.start()

################################################读取图像线程#################################################

def get_img():
    
    global ChestOrg_img, chest_ret
    image_reader_chest = ImgConverter()
    while True:
        chest_ret, ChestOrg_img = image_reader_chest.chest_image()
        #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        #print(ChestOrg_img)
        time.sleep(0.05)

# 读取图像线程
th1 = threading.Thread(target=get_img)
th1.setDaemon(True)
th1.start()


# def getAreaMaxContour1(contours):    # 返回轮廓 和 轮廓面积
#     contour_area_temp = 0
#     contour_area_max = 0
#     area_max_contour = None
#     for c in contours:  # 历遍所有轮廓
#         contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积
#         if contour_area_temp > contour_area_max:
#             contour_area_max = contour_area_temp
#             if contour_area_temp > 25:  #只有在面积大于25时，最大面积的轮廓才是有效的，以过滤干扰
#                 area_max_contour = c
#     return area_max_contour, contour_area_max  # 返回最大的轮廓

distance_x = 0

def follow_lines(cmd_ctrl):
    try:
        # 动作调用预设置
        # with serial.Serial('/dev/ttyAMA0', 115200) as ser:
        #     CMDcontrol.action_request(0,ser)

        print("Start action thread...")
        init_action_thread()    # 初始化动作线程
        time.sleep(1)
            
        global CMDcontrol
        CMDcontrol = cmd_ctrl
        # is_door_open = False
        global ChestOrg_img
        # global img_debug, step
        # step = 0
        while True :
            # if step == 0: #判断门是否抬起
            # t1 = cv2.getTickCount() # 时间计算
            #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            #print(ChestOrg_img)
            org_img_copy = ChestOrg_img.copy()
            org_img_copy = np.rot90(org_img_copy)
            frame = org_img_copy.copy()

            cv2.imshow("img", frame)
            cv2.waitKey(10)

            # 阈值处理
            threshold = 70
            # threshold = cv2.getTrackbarPos("threshold", "frame_gray")
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            threshold1, frame_threshold= cv2.threshold(frame_gray, threshold, 255, cv2.THRESH_BINARY_INV)
            #cv2.imshow("gray", frame_threshold)

            # 形态操作
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
            dil = cv2.dilate(frame_threshold, kernel, iterations = 1)
            #cv2.imshow("dil",dil)
            # clo = cv2.morphologyEx(frame_threshold, cv2.MORPH_CLOSE,kernel)
            # cv2.imshow("frame_gray",clo)

            # 塞选轮廓 并返回轮廓上y=400的点距中心点的偏差
            contours, hierarchy = cv2.findContours(dil, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            dot=np.array([[175,93]])
            for i in range(len(contours)):
                if cv2.contourArea(contours[i])>2000 and cv2.contourArea(contours[i])<10000:
                    for point in contours[i]:
                        if point[0][0] == 175:
                            dot = np.vstack((dot, point))
                    #cv2.drawContours(img_ROI, contours[i], -1, (0,255,0), 3)
            #cv2.imshow("img_ROI",img_ROI)
            # print(dot)
            average_x = 0   
            print("长度：",len(dot))
            for n in range(len(dot)-2):
                average_x += dot[n+1][1]
            if len(dot) > 1:
                average_x = average_x/(len(dot)-1)
            else:                 
                average_x = 93
            global distance_x 
            distance_x = dot[0][1]-average_x
            print(distance_x)
            # if distance_x > 50:
            #     action("turn004L")
            #     print("左转")
            #     time.sleep(1)
            #     action("Forwalk02RS")
            #     print("走2步")
            #     time.sleep(1)
            # if distance_x < -50:
            #     action("turn004R")
            #     print("右转")
            #     time.sleep(1)
            #     action("Forwalk02RS")
            #     print("走2步")
            #     time.sleep(1)
            # else:
            #     action("Forwalk02RS")
            #     print("走2步")
            #     time.sleep(1)
            action("Forwalk02")

    except rospy.ROSInterruptException:
        pass


#################################################################动作执行####################################
if __name__ == '__main__':
    follow_lines(CMDcontrol)

    # # 串口连接部分，目前这块有问题导致动作执行不了
    # with serial.Serial('/dev/ttyAMA0', 115200) as ser:
    #     CMDcontrol.action_request(0,ser)

    # print("Start action thread...")
    # init_action_thread()    # 初始化动作线程
    # time.sleep(1)

    # rospy.init_node('start_door_nodes')
    # time.sleep(3)
    # follow_lines(CMDcontrol)  # 调用主函数，循线代码

    

