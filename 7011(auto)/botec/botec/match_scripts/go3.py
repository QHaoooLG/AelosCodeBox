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
    'green': [(39 , 128 , 195), (45 , 162 , 255)],
    'orange': [(18, 218 , 38), (27 , 255 , 255)]
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
        time.sleep(0.3)
        if ChestOrg is not None:
            Chest_img = ChestOrg
            time.sleep(0.05)
            #Chest_img = cv2.flip(Chest_img, 1)
        else:
            time.sleep(0.3)
            print("暂时未获取到图像")
th2 = threading.Thread(target=get_img)
th2.setDaemon(True)
th2.start()

#查找方块
def find_box(img,color_name):
    global chest_circle_x, chest_circle_y
    if Chest_img is None:
        print('等待获取图像中...')
        time.sleep(0.3)
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
    global ID
    if chest_circle_x is None :
        print('等待中获取坐标中...')
        time.sleep(0.3)
    else:
        if chest_circle_x < 295: 
            print("正在左侧移 ",chest_circle_x)
            action.L_move1(1)
            time.sleep(0.5)
        elif chest_circle_x > 345:    
            print("正在右侧移 ",chest_circle_x)
            action.R_move1(1)
            time.sleep(0.5)
        else:
            if chest_circle_y < 330:  
                print("前进",chest_circle_y)
                action.go_slow(1)
                time.sleep(0.5)
            elif chest_circle_y >= 370:  
                print("后退",chest_circle_y)
                action.back_slow(1)
                time.sleep(0.5)
            else:
                print("开始抱箱子")
                action.go_slow(1)
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
            if ID == 1 or ID == 2 or ID == 3 or ID == 4 or ID == 5:
                action.box_back1(1)
            if ID == 6 or ID == 7:
                action.back_fast(1)
            if ID == 8:
                action.back_slow(1)
                action.L_move1(1)
            time.sleep(0.5)
        elif ID == marker[0]:
            tag_x.append(int(marker[1]*100))
            tag_y.append(int(marker[2]*100))
            tag_yaw.append(int(marker[3]))
        else:
            print('tag不匹配')
            print('ID',ID,'marker[0]',marker[0])
            if ID == 1 or ID == 3 or ID == 4:
                action.box_back1(1)
            if ID == 2 or ID == 5:
                action.box_go1(1)
            if ID == 6 :
                action.back_fast(1)
            if ID == 7:
                action.go_fast(1)
            if ID == 8:
                action.L_move1(1)
            time.sleep(0.5)

#空手时调整与tag之间的角度
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

#空手时调整与tag之间的距离
@timefn
def action_step(x_low,x_high,y_low,y_high):
    if avg_y < y_low:
        chg_y = y_low - avg_y
        y_step1 = int(chg_y / 5);y_step2 = math.ceil((chg_y - y_step1 * 5) / 1.5)
        print('Ry_step1=', y_step1, 'Ry_step2=', y_step2)
        action.R_move1(y_step2)
        action.R_move2(y_step1)
    elif avg_y > y_high:
        chg_y = avg_y - y_high
        y_step1 = int(chg_y / 5);y_step2 = math.ceil((chg_y - y_step1 * 5) / 1.5)
        print('Ly_step1=', y_step1, 'Ly_step2=', y_step2)
        action.L_move1(y_step2)
        action.L_move2(y_step1)
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

#抱着箱子时调整与tag之间的角度
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

#抱着箱子时调整与tag之间的距离
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


#计算A矩阵乘B矩阵  利用旋转矩阵补偿读取到的与tag的距离用到
def matrixMul(A, B):
    res = [[0] * len(B[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                res[i][j] += int(A[i][k] * B[k][j])
    return res


if __name__ == '__main__':
    rospy.init_node('image_listener')   #ROS节点初始化
    Tag = TagConverter()
    time.sleep(0.5)
    ID = 0      #选择开始时的位置,从初始位置开始各参数为：ID = 0,step = 1,n = 1
    step = 1
    n = 1      #若调试时从ID=2以后开始,需提前将n改为-1,step改为0
    while True:
        while ChestOrg is None:
            print('wite')
        if step == 1:  #从初始位置开始,搬箱子并走到tag1或tag2面前
            print('启动')
            action.go_fast(2)
            while True:
                if ID == 0:  #搬箱子
                    find_box(Chest_img, 'orange')
                    goto_box()
                    time.sleep(0.1)
                elif ID == 1:
                    break
            action.box_go2(7)
            action.box_R_turn2(2)
            while True:
                marker = Tag.get_nearest_marker()
                print('step1 get_marker')
                if len(marker) == 0:  #边转身边寻找tag,找到后检查角度时候合适
                    print('step1 marker空')
                    action.box_R_turn1(1)
                    action.box_R_move1(1)
                    time.sleep(0.5)
                elif marker [0] == 2 or marker [0] == 1: #无论看到的时tag1还是tag2都会调整位置
                    print(marker[3])
                    if marker[3] > -100:
                        print('step1 左转调整')
                        action.box_L_turn1(2)
                        action.box_L_move1(1)
                        time.sleep(0.5)
                    elif marker[3] < -115:
                        print('step1 右转调整')
                        action.box_R_turn1(2)
                        action.box_R_move1(1)
                        time.sleep(0.5)
                    else:
                        step = 0
                        ID = marker[0]    #根据看到的tag选择下一步
                        print('step1 结束,赋值ID=',marker[0])
                        break
        if step == 2:    #从tag1后面开始,去搬箱子,并返回到tag1或者tag2正面的过程
            print('step=',step)
            action.go_fast(1)
            while True:
                if ID == 0: #搬箱子
                    find_box(Chest_img, 'orange')
                    goto_box()
                elif ID == 1:
                    print('step2 搬箱子结束')
                    break
            action.box_L_turn2(4)
            while True:
                marker = Tag.get_nearest_marker()
                print('step2 get_marker')
                if len(marker) == 0:  #边转身边寻找tag,找到后检查角度时候合适
                    print('step2 marker空')
                    action.box_L_turn1(2)
                    action.box_L_move1(1)
                    time.sleep(0.5)
                elif marker [0] == 2 or marker [0] == 1:  #无论看到的时tag1还是tag2都会调整位置
                    print("step2 ID=", marker[0])
                    if marker[3] > -75:
                        print("step2 左转")
                        action.box_L_turn1(2)
                        action.box_L_move1(1)
                        time.sleep(0.5)
                    elif marker[3] < -115:
                        print("step2 右转")
                        action.box_R_turn1(2)
                        action.box_R_move1(1)
                        time.sleep(0.5)
                    else:
                        step = 0
                        ID = marker[0]   #根据看到的tag选择下一步
                        print('step2 结束,赋值ID=', marker[0])
                        break
            #action.box_go2(1)
            step = 0
        if ID == 1: #与tag1对正,n=1时将ID变为2,n=-1时跳到step2
            print('################ ID=1 start ################')
            if n == 1:  #正向对正
                print('开始 n=',n)
                get_marker(1)
                print('1-1:',avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-105, -85)
                box_action_step(12, 17, -2.5, 2.5)
                time.sleep(0.5)
                get_marker(1)
                print('1-2:',avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-105, -85)
                print('1第1次对正结束')
                time.sleep(0.5)
                get_marker(1)
                print('1-3:', avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-100,-90)
                box_action_step(3,9,-1.5,1.5)
                time.sleep(0.5)
                get_marker(1)
                print('1-4:', avg_x, avg_y, avg_yaw)
                box_action_step_yaw(-100,-90)
                print('1第2次对正结束')
                action.box_go2(2)
                n = -n
                print('n的值变为',n)
                ID+=1
            elif n == -1:  #反方向对正
                print('开始 n=', n)
                time.sleep(0.5)
                get_marker(1)
                action_step_yaw(80, 90)
                action_step(4,7,-2,2)
                get_marker(1)
                action_step_yaw(80, 90)
                print('1--1',avg_x, avg_y, avg_yaw)
                print('-1第1次对正结束')
                n = -n
                print('n的值变为', n)
                step = 2
                ID = 0
            print('################ ID=1 END ################')
        if ID == 2:  #与tag2对正并移动到tag3前面 将ID变为3
            print('################ ID=2 Start ################')
            time.sleep(0.5)
            get_marker(1)
            print('2-6:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-115,-75)
            print('2号码初始角度对正结束')
            time.sleep(0.5)
            get_marker(1)
            print('2-7:', avg_x, avg_y, avg_yaw)
            box_action_step(16, 20, -3, 3)
            print('2号码第一次距离对正结束')
            time.sleep(0.5)
            get_marker(1)
            print('2-8:', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-105, -93)
            box_action_step(8, 12, -3, 3)
            box_action_step_yaw(-96, -87)
            print('2号码最终角度及距离对正结束')
            action.box_R_move1(15)
            if n == -1:      #从step2直接进入ID2的时候省略的一个n取反的过程,所以在这里加一个判断
                print('无跳关 n=',n)
            elif n == 1:
                n = -n
                print('跳关 n=',n)
            ID+=1
            print('################ ID=2 END ################')
        if ID == 3:  #与tag3对正 将ID变为4或者5
            print('################ ID=3 Start ################')
            while True:
                marker = Tag.get_nearest_marker()
                if len(marker) == 0:
                    action.box_back1(1)
                    continue
                elif marker[0] == 3:
                    print('ID3 marker=', marker[0])
                    get_marker(1)
                    print('3-1:', avg_x, avg_y, avg_yaw)
                    box_action_step_yaw(-100,-90)
                    box_action_step(10, 13, -3, 3)
                    get_marker(1)
                    print('3-2', avg_x, avg_y, avg_yaw)
                    box_action_step_yaw(-100, -90)
                    print('3第1次对正结束')
                    action.box_R_move1(6)
                    ID+=1
                    break
                elif marker[0] == 5:
                    print('ID3 marker=', marker[0])
                    action.box_L_move2(2)
                    ID+=2
                    print('跳关3→5',ID)
                    break
            print('################ ID=3 END ################')
        if ID == 4: #与tag4对正 将ID变为5
            print('################ ID=4 Start ################')
            while True:
                marker = Tag.get_nearest_marker()
                if len(marker) == 0:
                    action.box_back1(1)
                    continue
                elif marker [0] == 4:
                    print('ID4 marker=',marker[0])
                    get_marker(1)
                    print('4-1', avg_x, avg_y, avg_yaw)
                    box_action_step_yaw(-100,-90)
                    box_action_step(10, 13, -1.5, 1.5)
                    get_marker(1)
                    print('4-2', avg_x, avg_y, avg_yaw)
                    box_action_step_yaw(-100, -90)
                    print(avg_x, avg_y, avg_yaw)
                    print('4第1次对正结束')
                    action.box_go2(2)
                    ID+=1
                    break
                elif marker [0] == 5:  #如果视野中看到的时tag5可以直接进入ID5
                    print('ID4 marker=', marker[0])
                    ID+=1
                    print('跳关4→5',ID)
                    break
            print('################ ID=4 END ################')
        if ID == 5:  #与tag5对正并移动到tag6前面 将ID变为6
            print('################ ID=5 Start ################')
            get_marker(1)
            print('5-3', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-100, -90)
            box_action_step(15, 22, -4, 4)
            get_marker(1)
            print('5-4', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-100, -90)
            print(avg_x, avg_y, avg_yaw)
            print('5第2次对正结束')
            get_marker(1)
            print('5-5', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-98, -92)
            box_action_step(10, 15, -3, 3)
            get_marker(1)
            print('5-6', avg_x, avg_y, avg_yaw)
            box_action_step_yaw(-98, -92)
            print(avg_x, avg_y, avg_yaw)
            print('5第3次对正结束')
            action.box_L_move2(12)
            ID+=1
            print('################ ID=5 END ################')
        if ID == 6:  #走到大本营将箱子放下,转身回来与tag6对正,并走到tag7前面 将ID变为7
            print('################ ID=6 Start ################')
            action.box_L_turn1(1)
            action.box_go2(6)
            action.box_down(1)
            action.R_turn3(3)  # 先转向3个45°,然后进行识别
            print('ID6 粗转结束')
            while True:
                marker = Tag.get_nearest_marker()
                if len(marker) == 0 : #边转身边寻找tag,找到后根据看到的tagID不同选择对正
                    print('ID6 marker 空')
                    action.R_turn2(2)
                    action.R_move2(1)
                    time.sleep(0.5)
                elif marker[0] == 7:   #正对着是 -95°   #修正与tag7的角度
                    print('ID6 marker=', marker[0])
                    if marker[3] > -75:
                        print('ID6-7 左转')
                        action.L_turn1(2)
                        action.L_move1(1)
                        time.sleep(0.5)
                    elif marker[3] < -115:
                        print('ID6-7 右转')
                        action.R_turn1(2)
                        action.R_move1(1)
                        time.sleep(0.5)
                    else:
                        ID+=1
                        print('ID6 结束,赋值ID=', marker[0])
                        break
                elif marker[0] == 6 :    #正对着是 85°   #修正与tag6的角度
                    print('ID6 marker=', marker[0])
                    if marker[3] < 65:
                        print('ID6-6 左转')
                        action.R_turn2(2)
                        action.R_move2(1)
                        time.sleep(0.5)
                    elif marker[3] > 105:
                        print('ID6-6 右转')
                        action.L_turn2(2)
                        action.L_move2(1)
                        time.sleep(0.5)
                    else:
                        print('ID6 矫正开始')
                        get_marker(1)
                        print('6-1', avg_x, avg_y, avg_yaw)
                        action_step_yaw(80, 90)
                        action_step(8, 12, -2, 2)
                        get_marker(1)
                        print('6-2', avg_x, avg_y, avg_yaw)
                        action_step_yaw(80, 90)
                        print(avg_x, avg_y, avg_yaw)
                        print('6第2次对正结束')
                        get_marker(1)
                        print('6-3', avg_x, avg_y, avg_yaw)
                        action_step_yaw(82, 87)
                        action_step(4, 7, -1.5, 1.5)
                        get_marker(1)
                        print('6-4', avg_x, avg_y, avg_yaw)
                        action_step_yaw(80, 90)
                        print(avg_x, avg_y, avg_yaw)
                        print('6第3次对正结束')
                        action.go_fast(2)
                        ID += 1
                        break
            print('################ ID=6 END ################')
        if ID == 7:  #与tag7对正并移动到tag4前面 将ID变为8
            print('################ ID=7 Start ################')
            get_marker(1)
            print('7-00', avg_x, avg_y, avg_yaw)
            action_step_yaw(-105, -85)
            action_step(22, 31, -4, 4)
            get_marker(1)
            print('7-0', avg_x, avg_y, avg_yaw)
            action_step_yaw(-105, -85)
            print(avg_x, avg_y, avg_yaw)
            print('7第0次对正结束')
            get_marker(1)
            print('7-1', avg_x, avg_y, avg_yaw)
            action_step_yaw(-100, -90)
            action_step(15, 18, -4, 4)
            get_marker(1)
            print('7-2', avg_x, avg_y, avg_yaw)
            action_step_yaw(-100, -90)
            print(avg_x, avg_y, avg_yaw)
            print('7第1次对正结束')
            get_marker(1)
            print('7-3', avg_x, avg_y, avg_yaw)
            action_step_yaw(-100, -90)
            action_step(10, 14, -3, 3)
            get_marker(1)
            print('7-4', avg_x, avg_y, avg_yaw)
            action_step_yaw(-100, -90)
            print(avg_x, avg_y, avg_yaw)
            print('7第2次对正结束')
            action.L_move2(8)
            ID+=1
            print('################ ID=7 END ################')
        if ID == 8: #直接前进到tag8前面
            print('################ ID=8 Start ################')
            action.L_turn1(1)
            action.go_fast3(1)
            #与tag8对正并移动到tag1后面 将ID变为1
            time.sleep(0.5)
            get_marker(1)
            print('8-1', avg_x, avg_y, avg_yaw)
            action_step_yaw(-105, -85)
            action_step(13, 16, -4, 4)
            get_marker(1)
            print('8-2', avg_x, avg_y, avg_yaw)
            action_step_yaw(-105, -85)
            print(avg_x, avg_y, avg_yaw)
            print('8第1次对正结束')
            get_marker(1)
            print('8-3', avg_x, avg_y, avg_yaw)
            action_step_yaw(-100, -90)
            action_step(8, 12, -3, 3)
            get_marker(1)
            print('8-4', avg_x, avg_y, avg_yaw)
            action_step_yaw(-100, -90)
            print(avg_x, avg_y, avg_yaw)
            print('8第2次对正结束')
            action.R_move2(4)
            action.L_turn1(1)
            action.R_move2(4)
            action.L_turn1(1)
            action.R_move2(4)
            action.go_fast(1)
            ID = 1
            print('################ ID=8 END ################')