#!/usr/bin/env python3
# coding:utf-8

import numpy as np
import cv2
# import math
# import serial
import threading
import time
# import datetime
import rospy
import CMDcontrol
# import tf
# from math import sqrt
# from geometry_msgs.msg import PoseWithCovarianceStamped
# from ar_track_alvar_msgs.msg import AlvarMarkers
# from ar_track_alvar_msgs.msg import AlvarMarker
# from startDoorOnly import start_door
from image_converter import ImgConverter
import hashlib


chest_r_width = 480
chest_r_height = 640
img_debug = True

action_DEBUG = False
CMDcontrol = None

chest_ret = True    
ChestOrg_img = None  

single_debug = 0

###################################动作线程初始化#####################################################

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


# distance_x = 0

# 动作添加到队列
acted_name = ""
def action_append(act_name):    
    global acted_name

    # print("please enter to continue...")
    # cv2.waitKey(0)

    if action_DEBUG == False:
        if act_name == "forwardSlow0403" and (acted_name == "Forwalk02RL" or acted_name == "Forwalk02L"):
            acted_name = "Forwalk02LR"
        elif act_name == "forwardSlow0403" and (acted_name == "Forwalk02LR" or acted_name == "Forwalk02R"):
            acted_name = "Forwalk02RL"
        elif act_name != "forwardSlow0403" and (acted_name == "Forwalk02LR" or acted_name == "Forwalk02R"):
            # CMDcontrol.action_list.append("Forwalk02RS")
            # acted_name = act_name
            print(act_name,"动作未执行 执行 Stand")
            acted_name = "Forwalk02RS"
        elif act_name != "forwardSlow0403" and (acted_name == "Forwalk02RL" or acted_name == "Forwalk02L"):
            # CMDcontrol.action_list.append("Forwalk02LS")
            # acted_name = act_name
            print(act_name,"动作未执行 执行 Stand")
            acted_name = "Forwalk02LS"
        elif act_name == "forwardSlow0403":
            acted_name = "Forwalk02R"
        else:
            acted_name = act_name

        
        m = hashlib.md5()
        name_encode = bytes(act_name,encoding='utf8')
        m.update(name_encode)
        acted_name = 'leju_' + m.hexdigest()
        print(acted_name)#fftest

        CMDcontrol.actionComplete = False
        if len(CMDcontrol.action_list) > 0:
            print("队列超过一个动作")
            CMDcontrol.action_list.append(acted_name)
        else:
            if single_debug:
                cv2.waitKey(0)
            CMDcontrol.action_list.append(acted_name)
        CMDcontrol.action_wait()
        time.sleep(1)

    else:
        print("-----------------------执行动作名：", act_name)
        time.sleep(1)

# 动作执行函数
def running_lines(distance_x):
    if distance_x > 30:
        action("turn003R")
        print("右转")
        time.sleep(1)
        action("fastForward03")
        print("走1步")
        time.sleep(0.5)
    elif distance_x < -30:
        action("turn003L")
        print("左转")
        time.sleep(1)
        action("fastForward03")
        print("走1步")
        time.sleep(0.5)
    else:
        action("fastForward03")
        print("走1步")
        time.sleep(0)

# 巡线主函数
def follow_lines(cmd_ctrl):

    # 动作调用预设置
    # with serial.Serial('/dev/ttyAMA0', 115200) as ser:
    #     CMDcontrol.action_request(0,ser)

    # print("Start action thread...")
    # init_action_thread()    # 初始化动作线程
    # time.sleep(1)
        
    global CMDcontrol
    CMDcontrol = cmd_ctrl
    # is_door_open = False
    global ChestOrg_img, step, img_debug
    # step =0
    while True :
        org_img_copy = ChestOrg_img.copy()
        org_img_copy = np.rot90(org_img_copy)
        frame = org_img_copy.copy()
        frame = cv2.resize(frame, (640,480))
        img_ROI = frame[133:320, 93:333]
        cv2.imshow("img", img_ROI)

        # 阈值处理
        threshold = 70
        # threshold = cv2.getTrackbarPos("threshold", "frame_gray")
        frame_gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
        
        threshold1, frame_threshold= cv2.threshold(frame_gray, threshold, 255, cv2.THRESH_BINARY_INV)
        cv2.imshow("gray", frame_threshold)

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
        distance_x = 0
        distance_x = dot[0][1]-average_x
        print(distance_x)

        running_lines(distance_x)
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
        # action("Forwalk02")

        cv2.waitKey(5)

#################################################################动作执行####################################

import CMDcontrol

# 串口连接部分，目前这块有问题导致动作执行不了
# with serial.Serial('/dev/ttyAMA0', 115200) as ser:
#     CMDcontrol.action_request(0,ser)

def thread_move_action():
    CMDcontrol.CMD_transfer()

th2 = threading.Thread(target=thread_move_action)
th2.setDaemon(True)
th2.start()

# print("Start action thread...")
# init_action_thread()    # 初始化动作线程
# time.sleep(1)

rospy.init_node('running_lines_node')
time.sleep(3)
action_append("Stand")
follow_lines(CMDcontrol)  # 调用主函数，循线代码