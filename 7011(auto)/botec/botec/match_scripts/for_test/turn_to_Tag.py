import time
import CMDcontrol as CMD
import cv2
import threading
import numpy as np
import rospy
import math
from image_Tag_converter import ImgConverter
from image_Tag_converter import TagConverter

real = 1
#动作指令监听线程
def move_action():
    if real :
        CMD.CMD_transfer()
th1 = threading.Thread(target=move_action)
th1.setDaemon(True)
th1.start()

def get_img():
    global Head_img
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

#前进#
def go_slow(n):   #慢速前进
    for i in range (0,n):
        CMD.action_append ("Forwalk00")
        time.sleep(2)
def go_fast(n):   #快速前进
    for i in range (0,n):
        CMD.action_append ("Forwalk01")
        time.sleep(0.7)
def box_go_slow(n):    #抱着箱子慢速前进
    for i in range (0,n):
        CMD.action_append ("boxForward")
        time.sleep(2)
def box_go_fast(n):     #抱着箱子快速前进
    for i in range (0,n):
        CMD.action_append ("boxForward6")
        time.sleep(0.3)
#后退#
def back_slow(n):      #慢速后退
    for i in range (0,n):
        CMD.action_append ("Back1Run")
        time.sleep(2)
def back_fast(n):      #快速后退
    for i in range (0,n):
        CMD.action_append ("Back2Run")
        time.sleep(2)
def box_back(n):      #抱着箱子后退
    for i in range (0,n):
        CMD.action_append ("boxBack")
        time.sleep(2)
#搬箱子#
def box_up (n):       #搬起箱子
    for i in  range (0,n):
        CMD.action_append ("boxUp0")
#放箱子#
def box_down_L (n):      #低位置放下箱子
    for i in  range (0,n):
        CMD.action_append ("boxDown1")
def box_down_M (n):      #中位置放下箱子
    for i in  range (0,n):
        CMD.action_append ("boxDown2")
def box_down_H (n):         #高位置放下箱子
    for i in  range (0,n):
        CMD.action_append ("boxDown3")
#踢箱子
def shoot_box (n):          #对着箱子踢一脚
    for i in  range (0,n):
        CMD.action_append ("Left_foot_shot")
#转向#
def L_move (n):           #左侧移
    for i in  range (0,n):
        CMD.action_append ("Left02move")
def R_move (n):           #右侧移
    for i in  range (0,n):
        CMD.action_append ("Right02move")
def L_turn (n):           #左转
    for i in  range (0,n):
        CMD.action_append ("turn004L")
def L_turn_slow (n):           #慢左转
    for i in  range (0,n):
        CMD.action_append ("turn001L")
def R_turn (n):           #右转
    for i in  range (0,n):
        CMD.action_append ("turn003R")
def R_turn_big (n):           #右转45°
    for i in  range (0,n):
        CMD.action_append ("turn010R")
        time.sleep(0.3)
def R_turn_slow (n):           #慢右转
    for i in  range (0,n):
        CMD.action_append ("turn001R")
def box_L_move (n):           #抱着箱子左侧移
    for i in  range (0,n):
        CMD.action_append ("boxLeft")
def box_R_move (n):           #抱着箱子右侧移
    for i in  range (0,n):
        CMD.action_append ("boxRight")
def box_L_turn (n):           #抱着箱子左转
    for i in  range (0,n):
        CMD.action_append ("boxTurnL")
def box_L_turn2 (n):           #抱着箱子左转2
    for i in  range (0,n):
        CMD.action_append ("boxTurnL2")
def box_R_turn (n):           #抱着箱子右转
    for i in  range (0,n):
        CMD.action_append ("boxTurnR")
        time.sleep(0.5)
def box_R_turn2 (n):           #抱着箱子右转2
    for i in  range (0,n):
        CMD.action_append ("boxTurnR2")
        time.sleep(0.5)

def L_avoid():    #左避障
    L_move(5)
    time.sleep(0.5)
    L_move(5)
    time.sleep(0.5)
    L_move(2)
    go_fast(4)
    R_move(1)
    R_turn(1)
    go_fast(4)
    R_move(1)
    R_turn(1)
def box_L_avoid():  #抱着箱子左避障
    box_L_move(12)
    box_go_fast(4)
    time.sleep(0.5)
    box_go_fast(2)
def R_avoid():  #右避障
    R_move(5)
    time.sleep(0.5)
    R_move(5)
    time.sleep(0.5)
    R_move(2)
    go_fast(4)
    R_move(1)
    R_turn(1)
    go_fast(4)
    R_move(1)
    R_turn(1)
def box_R_avoid():  #抱着箱子右避障
    box_R_move(12)
    box_go_fast(4)
    time.sleep(0.5)
    box_go_fast(2)

def turn_to_tag(dis_x, dis_y, theta, x_offset=0, y_offset=0, theta_offset=-90, x_threshold=0.09, y_threshold=0.015,theta_threshold=5):
    is_turn_done = False

    x_error = dis_x - x_offset
    y_error = dis_y - y_offset
    theta_error = theta - theta_offset
    print("theta:", theta, "theta_offset", theta_offset)
    print("x_error:", x_error, "y_error:", y_error, "theta_error:", theta_error)

    if (x_error < x_threshold - 0.03):
        print("1后退")
        back_fast(1)

    elif (y_error < -y_threshold - 0.10):
        print("1右移动")
        R_move(1)
    elif (y_error > y_threshold + 0.10):
        print("1左移动")
        L_move(1)

    elif (theta_error < -theta_threshold):
        print("1右转")
        R_turn_slow(1)
    elif (theta_error > theta_threshold):
        print("1左转")
        L_turn_slow(1)

    elif (y_error < -y_threshold):
        print("2右移动")
        R_move(1)
    elif (y_error > y_threshold):
        print("2左移动")
        L_move(1)

    elif (theta_error < -theta_threshold):
        print("2右转")
        R_turn_slow(1)
    elif (theta_error > theta_threshold):
        print("2左转")
        L_turn_slow(1)
    elif (x_error > x_threshold + 0.10):
        print("1前进")
        go_fast(1)

    # elif (x_error > x_threshold + 0.06):
    #     print("2前进")
    #     go_fast(1)
    # elif (x_error > x_threshold):
    #     print("2前进")
    #     go_slow(1)

    else:
        print("turn to tag ok")
        print("dis_x**:", dis_x, "dis_y**:", dis_y, "theta**:", theta)
        # time.sleep(5)
        is_turn_done = True

    return is_turn_done

def box_turn_to_tag(dis_x, dis_y, theta, x_offset=0, y_offset=0, theta_offset=-90, x_threshold=0.09, y_threshold=0.015,theta_threshold=5):
    is_turn_done = False

    x_error = dis_x - x_offset
    y_error = dis_y - y_offset
    theta_error = theta - theta_offset
    print("theta:", theta, "theta_offset", theta_offset)
    print("x_error:", x_error, "y_error:", y_error, "theta_error:", theta_error)

    if (x_error < x_threshold - 0.03):
        print("1后退")
        box_back(1)

    elif (y_error < -y_threshold - 0.10):
        print("1右移动")
        box_R_move(1)
    elif (y_error > y_threshold + 0.10):
        print("1左移动")
        box_L_move(1)

    elif (theta_error < -theta_threshold):
        print("1右转")
        box_R_turn(1)
    elif (theta_error > theta_threshold):
        print("1左转")
        box_L_turn(1)

    elif (y_error < -y_threshold):
        print("2右移动")
        box_R_move(1)
    elif (y_error > y_threshold):
        print("2左移动")
        box_L_move(1)

    elif (theta_error < -theta_threshold):
        print("2右转")
        box_R_turn(1)
    elif (theta_error > theta_threshold):
        print("2左转")
        box_L_turn(1)
    elif (x_error > x_threshold + 0.10):
        print("1前进")
        box_go_fast(1)


    # elif (x_error > x_threshold + 0.06):
    #     print("2前进")
    #     box_go_fast(1)
    # elif (x_error > x_threshold + 0.03):
    #     print("2前进")
    #     box_go_slow(1)

    else:
        print("turn to tag ok")
        print("dis_x**:", dis_x, "dis_y**:", dis_y, "theta**:", theta)
        # time.sleep(5)
        is_turn_done = True

    return is_turn_done

main_step = 2
Tag = TagConverter()
rospy.init_node('image_listener')
time.sleep(1)

while True:
    # print('第二步')
    marker = Tag.get_nearest_marker()
    if len(marker) == 0:
        box_L_turn2(1)
        time.sleep(0.5)
        box_L_move(2)
        continue
    robot_tag_x = marker[1]
    robot_tag_y = marker[2]
    tag_yaw = marker[3]
    result = box_turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw)
    if (result == False):
        continue
    main_step += 1
    print('矫正结束')
    break