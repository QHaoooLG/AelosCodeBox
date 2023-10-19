#!/usr/bin/env python3
# coding:utf-8

import numpy as np
import cv2
import threading
import time
import rospy
import CMDcontrol
import hashlib
from image_converter import ImgConverter


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
        time.sleep(0.05)

# 读取图像线程
th1 = threading.Thread(target=get_img)
th1.setDaemon(True)
th1.start()

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


# 巡线主函数
def follow_lines(cmd_ctrl):
    global CMDcontrol
    CMDcontrol = cmd_ctrl
    # is_door_open = False
    global ChestOrg_img, step, img_debug
    # step =0
    while True :
        org_img_copy = ChestOrg_img.copy()
        org_img_copy = np.rot90(org_img_copy)
        frame = org_img_copy.copy()
        frame = cv2.resize(frame, (480,640))
        frame_ROI = frame[230:640, 0:480]
        cv2.imshow("frame",frame)
        cv2.imshow("frame_ROI",frame_ROI)
        
        # 自适应阈值
        frame_gray = cv2.cvtColor(frame_ROI, cv2.COLOR_BGR2GRAY)
        frame_blur=cv2.GaussianBlur(frame_gray,(19,19),7)
        cv2.imshow("frame_blur",frame_blur)
        img_thresh_blur=cv2.adaptiveThreshold(frame_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,15,3)
        cv2.imshow("thresh",img_thresh_blur)

        # 塞选轮廓 并返回轮廓上y=400的点距中心点的偏差
        contours, hierarchy = cv2.findContours(img_thresh_blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        dot=np.array([[240,130]])
        for i in range(len(contours)):
            if cv2.contourArea(contours[i])>3000:
                for point in contours[i]:
                    if point[0][1] == 130:
                        dot = np.vstack((dot, point))
                cv2.drawContours(frame_ROI, contours[i], -1, (0,255,0), 3)
        cv2.imshow("img_ROI",frame_ROI)
        # print(dot)
        # print("长度：",len(dot))

        x = []
        for idx in range(len(dot)-1):
            x.append(dot[idx+1][0])
        x.sort()
        print(x)
        print(len(x))

        if len(x)>2:
            x_max=0
            x_min=0
            for n in range(len(x)//2):
                x_min = x[n] + x_min
                x_max = x[-(n+1)] + x_max
            x_max = x_max/(len(x)//2)
            x_min = x_min/(len(x)//2)

        elif len(x)==2:
            x_max = (x[0]+x[1])/2
            x_min = 0

        else:
           x_max = dot[0][0]
           x_min = dot[0][0]
        print("max=",x_max)
        print("min=",x_min)

        if dot[0][0]>x_max:
            action("turn005L")
            print("左转5度")
        elif dot[0][0]<x_min:
            action("turn005R")
            print("右转5度")
        else:
            action("fastForward03")
            print("走两步")
            
        cv2.destroyAllWindows()
        cv2.waitKey(0)

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