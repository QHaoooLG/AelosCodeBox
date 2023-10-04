import time
import CMDcontrol as CMD
import cv2
import threading
import numpy as np
import rospy
import math
from image_Tag_converter import ImgConverter
from image_Tag_converter import TagConverter

# 不同色块的hsv范围
color_range = {
    'red_box0': [(170,120,200),(190,140,260)],
    'red_box1': [(0, 128, 105), (45, 191, 170)],
    'red_box2': [(140, 128, 105), (179, 191, 170)],
    'red_box3': [(156, 43, 46), (180, 255, 255)]
}

real = 1
Head_img = None
ret = False
head_circle_x = None
head_circle_y = None

#动作指令监听线程
def move_action():
    if real :
        CMD.CMD_transfer()
th1 = threading.Thread(target=move_action)
th1.setDaemon(True)
th1.start()

#获取图像
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

#查找红色方块
def find_red_box(img,color_name):
    global head_circle_x, head_circle_y
    if Head_img is None:
        print('等待获取图像中...')
        time.sleep(1)
    else:
        red_box_img = img
        red_box_img_bgr = cv2.cvtColor(red_box_img, cv2.COLOR_RGB2BGR)  # 将图片转换到BRG空间
        red_box_img_hsv = cv2.cvtColor(red_box_img, cv2.COLOR_BGR2HSV)  # 将图片转换到HSV空间
        red_box_img = cv2.GaussianBlur(red_box_img_hsv, (3, 3), 0)  # 高斯模糊
        red_box_img_mask = cv2.inRange(red_box_img, color_range['red_box3'][0], color_range['red_box3'][1])  # 二值化
        red_box_img_closed = cv2.erode(red_box_img_mask, None, iterations=2)  # 腐蚀
        red_box_img_opened = cv2.dilate(red_box_img_mask, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算
        (contours, hierarchy) = cv2.findContours(red_box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            for cn in contours:
                (head_circle_x, head_circle_y), head_radius = cv2.minEnclosingCircle(cn)
                contour_area = math.fabs(cv2.contourArea(cn))
                max_cn = np.argmax(contour_area)
                if contour_area > 600 :
                    cv2.circle(red_box_img_bgr,(int(head_circle_x), int(head_circle_y)),int(head_radius),(0,0,255))

        else:
            print('正在寻找目标')
            L_turn_slow(1)

#根据ARTag码矫正(空手)
def turn_to_tag(dis_x, dis_y, theta, x_offset=0, y_offset=0, theta_offset=-90, x_threshold=0.09, y_threshold=0.015,theta_threshold=5):
    is_turn_done = False

    x_error = dis_x - x_offset
    y_error = dis_y - y_offset
    theta_error = theta - theta_offset
    print("theta:", theta, "theta_offset", theta_offset)
    print("x_error:", x_error, "y_error:", y_error, "theta_error:", theta_error)

    if (x_error < x_threshold - 0.03):
        print("1后退")
        back_fast(1)   #延迟2s

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
        go_fast(1)      #每步延迟0.7s

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

#根据ARTag码矫正（报箱子）
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


#去搬箱子
def goto_box():
    print('已经找到目标，准备调整位置')
    global main_step
    if head_circle_x is None :
        print('等待中获取坐标中...')
        time.sleep(1)
    else:
        if head_circle_y < 150:  # 240 - 50  (150)
            print("正在左侧移 ")
            L_move(1)
            time.sleep(1)
        elif head_circle_y > 220:    # 240 + 50  (220)
            print("正在右侧移 ")
            R_move(1)
            time.sleep(1)
        else:
            if head_circle_x > 180:  #320 + 20   (180)
                print("前进")
                go_slow(1)
                time.sleep(0.5)
            elif head_circle_x < 100:  #320 - 20 (100)
                print("后退")
                back_slow(1)
                time.sleep(0.5)
            else:
                print("开始抱箱子")
                R_move(1)
                box_up(1)
                main_step = main_step + 1
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
def L_turn_big (n):           #右转45°
    for i in  range (0,n):
        CMD.action_append ("turn010L")
        time.sleep(0.3)
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
        CMD.action_append ("boxturn009L2")
def box_L_turn2 (n):           #抱着箱子左转2
    for i in  range (0,n):
        CMD.action_append ("boxTurnL2")
def box_R_turn (n):           #抱着箱子右转
    for i in  range (0,n):
        CMD.action_append ("boxturn009R2")
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
    go_fast(4)   #每步之间延迟0.7s
    R_move(1)
    R_turn(1)
    go_fast(4)   #每步之间延迟0.7s
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
    go_fast(4)     #每步之间延迟0.7s
    R_move(1)
    R_turn(1)
    go_fast(4)   #每步之间延迟0.7s
    R_move(1)
    R_turn(1)
def box_R_avoid():  #抱着箱子右避障
    box_R_move(12)
    box_go_fast(4)
    time.sleep(0.5)
    box_go_fast(2)

if __name__ == '__main__':
    global main_step
    main_step = -1
    Tag = TagConverter()
    rospy.init_node('image_listener')
    time.sleep(1)
    while True:
        if main_step == -1:   #启动并抓取方块
            print('启动')
            R_turn_big(4)
            R_move(2)
            find_red_box(Head_img,'red_box')
            goto_box()
        if main_step == 0:   #向ARTag码对正(抱着箱子)
            print('第零步')
            marker = Tag.get_nearest_marker()
            if len(marker) == 0:
                box_R_turn2(1)
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
        if main_step == 1:   #对正方块并抓取
            print('第一步')
            find_red_box(Head_img,'red_box')
            goto_box()
        if main_step == 2:   #向ARTag码对正(抱着箱子)
            print('第二步')
            marker = Tag.get_nearest_marker()
            if len(marker) == 0:
                box_L_turn2(1)
                time.sleep(0.5)
                box_L_move(2)
                continue
            robot_tag_x = marker[1]
            robot_tag_y = marker[2]
            tag_yaw = marker[3]
            result = box_turn_to_tag(robot_tag_x,robot_tag_y,tag_yaw)
            if (result == False):
                continue
            main_step+=1
        if main_step == 3:   #避障(抱着箱子)
            print('第三步')
            box_L_avoid()
            main_step += 1
        if main_step == 4:   #右侧移(抱着箱子)
            print('第四步')
            box_R_move(6) #8
            main_step += 1
        if main_step == 5:    #向ARTag码对正(抱着箱子)
            print('第五步')
            marker = Tag.get_nearest_marker()
            if len(marker) == 0:
                box_R_move(1)
                continue
            robot_tag_x = marker[1]
            robot_tag_y = marker[2]
            tag_yaw = marker[3]
            result = box_turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw)
            if (result == False):
                continue
            main_step += 1
        if main_step == 6:  #避障(抱着箱子)
            print('第六步')
            box_R_avoid()
            main_step += 1
        if main_step == 7:  #左侧移(抱着箱子)
            print('第七步')
            box_L_move(3)
            main_step += 1
        if main_step == 8:  #向ARTag码对正(抱着箱子)
            print('第八步')
            marker = Tag.get_nearest_marker()
            if len(marker) == 0:
                box_L_move(1)
                continue
            robot_tag_x = marker[1]
            robot_tag_y = marker[2]
            tag_yaw = marker[3]
            result = box_turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw)
            if (result == False):
                continue
            main_step += 1
        if main_step == 9:  #避障(抱着箱子)
            print('第九步')
            box_L_avoid()
            main_step += 1
        if main_step == 10:   #放下箱子并踢走
            print('第十步')
            box_down_H(1)
            go_fast(2)   #每步之间0.7s延迟
            main_step += 1
        if main_step == 11:
            print('第十一步')
            R_turn_big(4)  #每步之间0.3s延迟
            R_move(2)
            main_step += 1
        if main_step == 12:   #前进，左侧移
            print('第十二步')
            go_fast(4)    #每步之间0.7s延迟
            R_move(1)
            R_turn(1)
            go_fast(4)    #每步之间0.7s延迟
            R_move(1)
            R_turn(1)
            go_fast(4)    #每步之间0.7s延迟
            R_move(1)
            R_turn(1)
            L_move(2)
            main_step += 1
        if main_step == 13:  #向ARTag码对正
            print('第十三步')
            marker = Tag.get_nearest_marker()
            if len(marker) == 0:
                L_move(1)
                continue
            robot_tag_x = marker[1]
            robot_tag_y = marker[2]
            tag_yaw = marker[3]
            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw)
            if (result == False):
                continue
            main_step += 1
        if main_step == 14:   #避障
            print('第十四步')
            L_avoid()
            main_step += 1
        if main_step == 15:   #右侧移
            print('第十五步')
            R_move(6)
            time.sleep(0.5)
            R_move(2)
            main_step += 1
        if main_step == 16:   #向ARTag码对正
            print('第十六步')
            marker = Tag.get_nearest_marker()
            if len(marker) == 0:
                R_move(1)
                continue
            robot_tag_x = marker[1]
            robot_tag_y = marker[2]
            tag_yaw = marker[3]
            result = turn_to_tag(robot_tag_x, robot_tag_y, tag_yaw)
            if (result == False):
                continue
            main_step += 1
        if main_step == 17:   #避障
            print('第十七步')
            R_avoid()
            go_fast(4)   #每步之间0.7s延迟
            R_move(1)
            R_turn(1)
            L_turn_big(2) #每步之间0.3s延迟
            main_step = 1

