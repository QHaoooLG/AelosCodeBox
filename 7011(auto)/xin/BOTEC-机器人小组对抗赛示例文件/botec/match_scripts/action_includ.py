import CMDcontrol as CMD
import time

################# 包含botac比赛用到的全部动作 #################

#前进#
def go_slow(n):   #慢速前进   前进2.5cm
    for i in range (0,n):
        CMD.action_append ("Forwalk00")
        print('前进2.5cm')
def go_fast(n):   #快速前进  前进4.5cm
    for i in range (0,n):
        CMD.action_append ("Forwalk01")
        print('前进4.5cm')
def go_fast3(n):   #快速前进  前进32cm
    for i in range (0,n):
        CMD.action_append ("fastForward03")
        print('前进32cm')
def box_go1(n):    #抱着箱子前进   前进4cm
    for i in range (0,n):
        CMD.action_append ("boxForward0.5")
        print('前进4cm')
def box_go2(n):     #抱着箱子前进  前进8cm
    for i in range (0,n):
        CMD.action_append ("boxForward")
        time.sleep(0.3)
        print('前进8cm')


#后退#
def back_slow(n):      #慢速后退  后退2.5cm
    for i in range (0,n):
        CMD.action_append ("Back1Run")
        print('后退2.5cm')
def back_fast(n):      #快速后退  后退4.5cm
    for i in range (0,n):
        CMD.action_append ("Back2Run")
        print('后退4.5cm')
def box_back1(n):      #抱着箱子后退  后退3.5cm
    for i in range (0,n):
        CMD.action_append ("boxBack0.5")
        print('后退3.5cm')
def box_back2(n):      #抱着箱子后退  后退7cm
    for i in range (0,n):
        CMD.action_append ("boxBack")
        print('后退7cm')


#搬箱子#
def box_up (n):       #搬起箱子
    for i in  range (0,n):
        CMD.action_append ("box_up6")
        print('搬起箱子')
#放箱子#
def box_down (n):         #高位置放下箱子
    for i in  range (0,n):
        CMD.action_append ("boxDown3")
        print('放下箱子')


#侧移#
def L_move1 (n):           #左侧移  左移1.5cm
    for i in  range (0,n):
        CMD.action_append ("Left02move")
        print('左移1.5cm')
def L_move2 (n):           #左侧移  左移5cm
    for i in  range (0,n):
        CMD.action_append ("Left3move")
        time.sleep(0.3)
        print('左移5cm')
def R_move1 (n):           #右侧移  右移1.5cm
    for i in  range (0,n):
        CMD.action_append ("Right02move")
        print('右移1.5cm')
def R_move2 (n):           #右侧移  右移5cm
    for i in  range (0,n):
        CMD.action_append ("Right3move")
        time.sleep(0.5)
        print('右移5cm')


#转向#
def L_turn1 (n):           #左转  左转7°
    for i in  range (0,n):
        CMD.action_append ("turn001L")
        print('左转7°')
def L_turn2 (n):           #左转  左转15°
    for i in  range (0,n):
        CMD.action_append ("turn004L")
        print('左转15°')
def L_turn3(n):           #左转  左转45°
    for i in  range (0,n):
        CMD.action_append ("turn010L")
        print('左转45°')
def R_turn1 (n):           #右转  右转7°
    for i in  range (0,n):
        CMD.action_append ("turn001R")
        print('右转7°')
def R_turn2 (n):           #右转   右转15°
    for i in  range (0,n):
        CMD.action_append ("turn003R")
        print('右转15°')
def R_turn3 (n):           #右转    右转45°
    for i in  range (0,n):
        CMD.action_append ("turn010R")
        print('右转45°')


#搬箱子侧移#
def box_L_move1 (n):   #抱着箱子左侧移     左移1.5
    for i in  range (0,n):
        CMD.action_append ("boxLeft")
        print('搬箱子_左侧移1.5cm')
def box_L_move2 (n):   #抱着箱子左侧移    左移3.5cm
    for i in  range (0,n):
        CMD.action_append ("Left3move_04253")
        time.sleep(0.5)
        print('搬箱子_左侧移3.5cm')
def box_R_move1 (n):   #抱着箱子右侧移     右移3cm
    for i in  range (0,n):
        CMD.action_append ("boxRight")
        print('搬箱子_右侧移3cm')


#搬箱子转向#
def box_L_turn1 (n):           #抱着箱子左转   左转8°
    for i in  range (0,n):
        CMD.action_append ("boxturn009L")
        print('box_左转8°')
def box_L_turn2 (n):           #抱着箱子左转   左转24°
    for i in  range (0,n):
        CMD.action_append ("boxTurnL2")
        print('box_左转24°')
def box_R_turn1 (n):           #抱着箱子右转    右转7°
    for i in  range (0,n):
        CMD.action_append ("boxturn009R")
        print('box_右转8°')
def box_R_turn2 (n):           #抱着箱子右转2   右转30°
    for i in  range (0,n):
        CMD.action_append ("boxTurnR2")
        print('box_右转30°')


#其他动作
def head():  #挠头
    CMD.action_append('Scratch_head')
def Stand():   #站立
    CMD.action_append('Stand_up')
def test(n):
    for i in range(n):
        CMD.action_append('fastForward04')