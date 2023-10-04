import time
import CMDcontrol as CMD
import cv2
import threading
import numpy as np
import rospy
import math
from functools import wraps

from image_Tag_converter import ImgConverter
from image_Tag_converter import TagConverter
import action_includ as action

#定义一些参数
Chest_img = None
ChestOrg = None

marker = None
avg_x = None
avg_y = None
avg_yaw = None

chest_circle_x = None
chest_circle_y = None

real = 1

# 不同色块的hsv范围
color_range = {
    'red_box': [(156,43,46),(180,255,255)],
    'orange': [(16,139,86),(31,215,255)]
}

def timefn(fn):
    """计算性能的修饰器"""
    #
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f" {fn.__name__} took {t2 - t1: .5f} s")
        return result

    return measure_time

#动作指令监听线程
def move_action():
    if real :
        CMD.CMD_transfer()
th1 = threading.Thread(target=move_action)
th1.setDaemon(True)
th1.start()

#获取图像
def get_img():
    global Chest_img,ChestOrg
    global ret
    image_reader_chest = ImgConverter()
    while True:
        ret, ChestOrg = image_reader_chest.chest_image()
        time.sleep(1)
        if ChestOrg is not None:
            Chest_img = ChestOrg
            time.sleep(0.05)
            #Chest_img = cv2.flip(Chest_img, 1)
        else:
            time.sleep(1)
            print("暂时未获取到图像")
th2 = threading.Thread(target=get_img)
th2.setDaemon(True)
th2.start()

#查找方块
def find_box(img,color_name):
    global chest_circle_x, chest_circle_y
    if Chest_img is None:
        print('等待获取图像中...')
        time.sleep(1)
    else:
        box_img = img
        box_img_bgr = cv2.cvtColor(box_img, cv2.COLOR_RGB2BGR)  # 将图片转换到BRG空间
        box_img_hsv = cv2.cvtColor(box_img, cv2.COLOR_BGR2HSV)  # 将图片转换到HSV空间
        box_img = cv2.GaussianBlur(box_img_hsv, (3, 3), 0)  # 高斯模糊
        box_img_mask = cv2.inRange(box_img, color_range[color_name][0], color_range[color_name][1])  # 二值化
        box_img_closed = cv2.erode(box_img_mask, None, iterations=2)  # 腐蚀
        box_img_opened = cv2.dilate(box_img_mask, np.ones((4, 4), np.uint8), iterations=2)  # 膨胀    先腐蚀后运算等同于开运算
        (contours, hierarchy) = cv2.findContours(box_img_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            area = []
            for cn in contours:
                contour_area = math.fabs(cv2.contourArea(cn))
                area.append(contour_area)
            max_index = np.argmax(area)
            (chest_circle_x,chest_circle_y),chest_radius = cv2.minEnclosingCircle(contours[max_index])
            cv2.circle(img,(int(chest_circle_x),int(chest_circle_y)),int(chest_radius),(0,0,255))
            print('A','x=',chest_circle_x,'y=',chest_circle_y)
            cv2.imwrite('image.png',img)
        else:
            print('正在寻找目标')

#去搬箱子
def goto_box():
    print('已经找到目标，准备调整位置')
    global ID
    if chest_circle_x is None :
        print('等待中获取坐标中...')
        time.sleep(1)
    else:
        if chest_circle_y < 225:  # 240 - 50  (150)
            print("正在左侧移 ",chest_circle_y)
            action.L_move1(1)
            time.sleep(0.5)
        elif chest_circle_y > 275:    # 240 + 50  (220)
            print("正在右侧移 ",chest_circle_y)
            action.R_move1(1)
            time.sleep(0.5)
        else:
            if chest_circle_x > 210:  #320 + 20   (180)
                print("前进",chest_circle_x)
                action.go_slow(1)
                time.sleep(0.5)
            elif chest_circle_x < 155:  #320 - 20 (100)
                print("后退",chest_circle_x)
                action.back_slow(1)
                time.sleep(0.5)
            else:
                print("开始抱箱子")
                action.R_move1(1)
                action.box_up(1)
                ID+=1

#获取ARtag信息并处理
@timefn
def get_marker(key):
    global marker,avg_x,avg_y,avg_yaw,ID
    marker = []
    tag_x, tag_y, tag_yaw = [], [], []
    while key:
        marker = Tag.get_nearest_marker()
        if len(tag_x) == 3:
            avg_x = np.mean(tag_x)
            avg_y = np.mean(tag_y)
            avg_yaw = np.mean(tag_yaw)
            if avg_yaw < 0:
                rad_z = -avg_yaw - 90
            else:
                rad_z = -avg_yaw + 85
            rad_z = rad_z/180*math.pi
            mat_a = [[math.cos(rad_z),-math.sin(rad_z),0],[math.sin(rad_z),math.cos(rad_z),0],[0,0,1]]
            mat_b = [[avg_x],[avg_y],[0]]
            res = matrixMul(mat_a,mat_b)
            avg_x = res[0][0]
            avg_y = res[1][0]
            key = 0
        elif len(marker) == 0:
            print('无Tag')
            time.sleep(1)
            if ID == 2 or ID == 3 or ID == 4 or ID == 5:
                action.box_back1(1)
            if ID == 6 or ID == 7:
                action.back_fast(1)
            if ID == 9:
                action.L_move1(1)
            continue
        elif ID == marker[0]:
            tag_x.append(int(marker[1]*100))
            tag_y.append(int(marker[2]*100))
            tag_yaw.append(int(marker[3]))
        else:
            print('tag不匹配')
            print('ID',ID,'marker[0]',marker[0])
            time.sleep(1)
            if ID == 2 or ID == 3 or ID == 4 or ID == 5:
                action.box_back1(1)
            if ID == 6 or ID == 7:
                action.back_fast(1)
            if ID == 9:
                action.L_move1(1)
@timefn
def action_step_yaw(yaw_low,yaw_high):
    if avg_yaw < yaw_low:
        chg_yaw = yaw_low - avg_yaw
        yaw_step1 = int(chg_yaw / 15);yaw_step2 = math.ceil((chg_yaw - yaw_step1 * 15) / 7)
        print('Ryaw_step1=',yaw_step1,'Ryaw_step2=',yaw_step2)
        action.R_turn2(yaw_step1)
        action.R_turn1(yaw_step2)
    elif avg_yaw > yaw_high:
        chg_yaw = avg_yaw - yaw_high
        yaw_step1 = int(chg_yaw / 15);yaw_step2 = math.ceil((chg_yaw - yaw_step1 * 15) / 7)
        print('Lyaw_step1=', yaw_step1, 'Lyaw_step2=', yaw_step2)
        action.L_turn2(yaw_step1)
        action.L_turn1(yaw_step2)
@timefn
def action_step(x_low,x_high,y_low,y_high):
    if avg_y < y_low:
        chg_y = y_low - avg_y
        y_step = math.ceil(chg_y / 1.5)
        print('Ry_step',y_step)
        action.R_move1(y_step)
    elif avg_y > y_high:
        chg_y = avg_y - y_high
        y_step = math.ceil(chg_y / 1.5)
        print('Ly_step', y_step)
        action.L_move1(y_step)
    if avg_x < x_low:
        chg_x = x_low - avg_x
        x_step1 = int(chg_x / 4.5);x_step2 = math.ceil((chg_x - x_step1 * 4.5) / 2.5)
        print('Bx_step1=', x_step1, 'Bx_step2=', x_step2)
        action.back_fast(x_step1)
        action.back_slow(x_step2)
    elif avg_x > x_high:
        chg_x = avg_x - x_high
        x_step1 = int(chg_x / 4.5);x_step2 = math.ceil((chg_x - x_step1 * 4.5) / 2.5)
        print('Fx_step1=', x_step1, 'Fx_step2=', x_step2)
        action.go_fast(x_step1)
        action.go_slow(x_step2)

@timefn
def box_action_step_yaw(yaw_low,yaw_high):
    if avg_yaw < yaw_low:
        chg_yaw = yaw_low - avg_yaw
        yaw_step1 = math.ceil(chg_yaw / 7)
        print('Ryaw_step1=',yaw_step1)
        action.box_R_turn1(yaw_step1)
    elif avg_yaw > yaw_high:
        chg_yaw = avg_yaw - yaw_high
        yaw_step1 = math.ceil(chg_yaw / 8)
        print('Lyaw_step1=', yaw_step1)
        action.box_L_turn1(yaw_step1)
@timefn
def box_action_step(x_low,x_high,y_low,y_high):
    if avg_y < y_low:
        chg_y = y_low - avg_y
        y_step = math.ceil(chg_y / 3)
        print('Ry_step',y_step)
        action.box_R_move1(y_step)
    elif avg_y > y_high:
        chg_y = avg_y - y_high
        y_step1 = int(chg_y / 3.5);y_step2 = math.ceil((chg_y - y_step1 * 3.5) / 1.5)
        print('Ly_step1', y_step1,'Ly_step2',y_step2)
        action.box_L_move2(y_step1)
        action.box_L_move1(y_step2)
    if avg_x < x_low:
        chg_x = x_low - avg_x
        x_step1 = int(chg_x / 7);x_step2 = math.ceil((chg_x - x_step1 * 7) / 3.5)
        print('Bx_step1=', x_step1,'Bx_step2=', x_step2)
        action.box_back2(x_step1)
        action.box_back1(x_step2)
    elif avg_x > x_high:
        chg_x = avg_x - x_high
        x_step1 = int(chg_x / 8);x_step2 = math.ceil((chg_x - x_step1 * 8) / 4)
        print('Fx_step1=', x_step1, 'Fx_step2=', x_step2)
        action.box_go2(x_step1)
        action.box_go1(x_step2)



def matrixMul(A, B):   #矩阵相乘
    res = [[0] * len(B[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                res[i][j] += int(A[i][k] * B[k][j])
    return res


if __name__ == '__main__':
    rospy.init_node('image_listener')
    Tag = TagConverter()
    time.sleep(1)
    ID = 0
    step = 1
    n = 1
    while True:
        while ChestOrg is None:
            print('wite')
        if step == 1:  #转身寻找方块
            print('启动')
            # action.R_turn3(4)
            # action.R_move1(2)
            action.go_fast(2)
            while True:
                if ID == 0:
                    find_box(Chest_img, 'orange')
                    goto_box()
                elif ID == 1:
                    break
            action.box_go2(6)     #参数待修改
            action.box_R_turn2(2)
            while True:
                marker = Tag.get_nearest_marker()
                if len(marker) == 0 or marker[0] != 1:
                    action.box_R_turn1(1)
                    action.box_R_move1(1)
                    time.sleep(1)
                else:
                    step = 0
                    break
        if step == 2:
            action.go_fast(1)
            while True:
                if ID == 0:
                    find_box(Chest_img, 'orange')
                    goto_box()
                elif ID == 1:
                    break
            action.box_L_turn2(5)
            while True:
                marker = Tag.get_nearest_marker()
                if len(marker) == 0 or marker[0] != 1:
                    action.box_L_turn1(1)
                    action.box_L_move1(1)
                    time.sleep(1)
                else:
                    step = 0
                    break
            action.box_go2(1)
            step = 0
        if ID == 1:
            if n == 1:
                get_marker(1)
                print('1:',avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-100, -80)
                box_action_step(12, 17, -2.5, 2.5)
                time.sleep(1)
                get_marker(1)
                print('2:',avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-100, -80)
                print('1第1次对正结束')
                time.sleep(1)
                get_marker(1)
                print('3:', avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-95,-85)
                box_action_step(2,5,-1.5,1.5)
                time.sleep(1)
                get_marker(1)
                print('4:', avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-95,-85)
                print('1第2次对正结束')
                action.box_go2(2)
                n = -n
                ID+=1
            elif n == -1:
                time.sleep(1)
                get_marker(1)
                action_step_yaw(80, 90)
                action_step(4,7,-2,2)
                get_marker(1)
                action_step_yaw(80, 90)
                print(avg_x, avg_y, avg_yaw)
                print('-1第1次对正结束')
                step = 2
                ID = 0
                n = -n
        if ID == 2:
            time.sleep(1)
            get_marker(1)
            print('1:',avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-100, -80)
            box_action_step(35, 40, -4, 4)
            time.sleep(1)
            get_marker(1)
            print('2:',avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-100, -80)
            print('2第0次对正结束')
            time.sleep(1)
            get_marker(1)
            print('3:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-95,-85)
            box_action_step(25, 35, -4, 4)
            time.sleep(1)
            get_marker(1)
            print('4:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-95,-85)
            print('2第1次对正结束')
            time.sleep(1)
            get_marker(1)
            print('5:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-95,-85)
            box_action_step(15, 18, -4, 4)
            time.sleep(1)
            get_marker(1)
            print('6:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-95,-85)
            print('2第2次对正结束')
            time.sleep(1)
            get_marker(1)
            print('7:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-93,-87)
            box_action_step(10, 13, -3, 3)
            time.sleep(1)
            get_marker(1)
            print('8:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-93, -87)
            print('2第3次对正结束')
            action.box_R_move1(11)
            ID+=1
        if ID == 3:
            get_marker(1)
            box_action_step_yaw(-95,-85)
            box_action_step(7, 10, -3, 3)
            get_marker(1)
            box_action_step_yaw(-95, -85)
            print(avg_x, avg_y, avg_yaw)
            print('3第1次对正结束')
            action.box_R_move1(6)
            ID+=1
        if ID == 4:
            get_marker(1)
            box_action_step_yaw(-95,-85)
            box_action_step(7, 10, -1.5, 1.5)
            get_marker(1)
            box_action_step_yaw(-95, -85)
            print(avg_x, avg_y, avg_yaw)
            print('4第1次对正结束')
            action.box_go2(2)
            ID+=1
        if ID == 5:
            get_marker(1)
            box_action_step_yaw(-100, -80)
            box_action_step(31, 40, -4, 4)
            get_marker(1)
            box_action_step_yaw(-100, -80)
            print(avg_x, avg_y, avg_yaw)
            print('5第0次对正结束')
            get_marker(1)
            box_action_step_yaw(-95, -85)
            box_action_step(22, 31, -4, 4)
            get_marker(1)
            box_action_step_yaw(-95, -85)
            print(avg_x, avg_y, avg_yaw)
            print('5第1次对正结束')
            get_marker(1)
            box_action_step_yaw(-95, -85)
            box_action_step(13, 22, -4, 4)
            get_marker(1)
            box_action_step_yaw(-95, -85)
            print(avg_x, avg_y, avg_yaw)
            print('5第2次对正结束')
            get_marker(1)
            box_action_step_yaw(-93, -87)
            box_action_step(10, 13, -3, 3)
            get_marker(1)
            box_action_step_yaw(-93, -87)
            print(avg_x, avg_y, avg_yaw)
            print('5第3次对正结束')
            action.box_L_move2(12)
            ID+=1
        if ID == 6:
            action.box_L_turn1(1)
            action.box_go2(6)
            action.box_down(1)
            action.R_turn3(3)  # 先转向3个45°,然后进行识别
            while True:
                marker = Tag.get_nearest_marker()
                if len(marker) == 0 or marker[0] != 6:
                    action.R_turn2(1)
                    action.R_move2(1)
                    time.sleep(1)
                else:
                    get_marker(1)
                    action_step_yaw(78, 92)
                    action_step(12, 15, -3, 3)
                    get_marker(1)
                    action_step_yaw(78, 92)
                    print(avg_x, avg_y, avg_yaw)
                    print('6第2次对正结束')
                    get_marker(1)
                    action_step_yaw(80, 90)
                    action_step(8, 12, -2, 2)
                    get_marker(1)
                    action_step_yaw(80, 90)
                    print(avg_x, avg_y, avg_yaw)
                    print('6第2次对正结束')
                    get_marker(1)
                    action_step_yaw(82, 87)
                    action_step(4, 7, -1.5, 1.5)
                    get_marker(1)
                    action_step_yaw(80, 90)
                    print(avg_x, avg_y, avg_yaw)
                    print('6第2次对正结束')
                    action.go_fast(1)
                    ID += 1
                    break
        if ID == 7:
            get_marker(1)
            action_step_yaw(-100, -80)
            action_step(15, 18, -4, 4)
            get_marker(1)
            action_step_yaw(-100, -80)
            print(avg_x, avg_y, avg_yaw)
            print('7第1次对正结束')
            get_marker(1)
            action_step_yaw(-95, -85)
            action_step(10, 13, -3, 3)
            get_marker(1)
            action_step_yaw(-95, -85)
            print(avg_x, avg_y, avg_yaw)
            print('7第2次对正结束')
            action.L_move2(8)
            ID+=1
        if ID == 8:
            action.L_turn1(1)
            action.go_fast3(1)
            ID = 9
        if ID == 9:
            time.sleep(1)
            get_marker(1)
            action_step_yaw(-100, -80)
            action_step(13, 16, -4, 4)
            get_marker(1)
            action_step_yaw(-100, -80)
            print(avg_x, avg_y, avg_yaw)
            print('9第1次对正结束')
            get_marker(1)
            action_step_yaw(-95, -85)
            action_step(8, 12, -3, 3)
            get_marker(1)
            action_step_yaw(-97, -82)
            print(avg_x, avg_y, avg_yaw)
            print('9第2次对正结束')
            action.R_move2(4)
            action.L_turn1(1)
            action.R_move2(4)
            action.L_turn1(1)
            action.R_move2(4)
            action.go_fast(1)
            ID = 1