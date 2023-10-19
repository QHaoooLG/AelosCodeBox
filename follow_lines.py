import numpy as np
import cv2
import math
import threading
import time
import datetime
import rospy
import CMDcontrol


def Nothing(x):
    pass

cv2.namedWindow("frame_gray")
cv2.createTrackbar("threshold", "frame_gray", 0, 255, Nothing)


def action(act_name):
    print(f'执行动作: {act_name}')
    time.sleep(1)
    CMDcontrol.action_append(act_name) 


# 调用摄像头
cap=cv2.VideoCapture("http://192.168.43.218:8080/usb_cam_chest/image_raw")
cap.set(3, 640)
cap.set(4, 480)
while True:
    frame=cap.read()
    img_ROI = frame[133:320, 93:333]
    cv2.imshow("img",frame)

    # 阈值处理
    threshold = 70
    # threshold = cv2.getTrackbarPos("threshold", "frame_gray")
    frame_gray = cv2.cvtColor(img_ROI, cv2.COLOR_BGR2GRAY)
    cv2.imshow("img",frame_gray)
    threshold1, frame_threshold= cv2.threshold(frame_gray, threshold, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("gray", frame_threshold)

    # 形态操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dil = cv2.dilate(frame_threshold, kernel, iterations = 1)
    cv2.imshow("dil",dil)
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
            cv2.drawContours(img_ROI, contours[i], -1, (0,255,0), 3)
    cv2.imshow("img_ROI",img_ROI)
    # print(dot)
    average_x = 0
    print("长度：",len(dot))
    for n in range(len(dot)-2):
        average_x += dot[n+1][1]
    if len(dot) > 1:
        average_x = average_x/(len(dot)-1)
    else:
        average_x = 93
    distance_x = dot[0][1]-average_x
    print(distance_x)

    # 动作执行
    if distance_x > 50:
        action("turn004L")
        print("左转")
        time.sleep(1)
        action("Forwalk02RS")
        print("走2步")
        time.sleep(1)
    if distance_x < -50:
        action("turn004R")
        print("右转")
        time.sleep(1)
        action("Forwalk02RS")
        print("走2步")
        time.sleep(1)
    else:
        action("Forwalk02RS")
        print("走2步")
        time.sleep(1)

cap.release()
cv2.destroyAllWindows()
