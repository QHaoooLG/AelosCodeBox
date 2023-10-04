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

Head_img = None
marker = None
tag_x = 0
tag_y = 0
tag_yaw = 0

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

real = 1
#动作指令监听线程
def move_action():
    if real :
        CMD.CMD_transfer()
th1 = threading.Thread(target=move_action)
th1.setDaemon(True)
th1.start()

@timefn
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

@timefn
def get_marker():
    global marker,tag_x,tag_y,tag_yaw
    Tag = TagConverter()
    while True:
        marker = Tag.get_nearest_marker()
        if len(marker) == 0:
            tag_x,tag_y,tag_yaw = 0,0,0
            continue
        tag_x = marker[1]
        tag_y = marker[2]
        tag_yaw = marker[3]
th3 = threading.Thread(target=get_marker)
th3.setDaemon(True)
th3.start()


if __name__ == '__main__':
    rospy.init_node('image_listener')
    time.sleep(1)
    while True:
        if tag_x == 0 and tag_y == 0:
            print('无Tag')
        else:
            print(marker)
            # print('x=',tag_x,'y=',tag_y,'θ=',tag_yaw)