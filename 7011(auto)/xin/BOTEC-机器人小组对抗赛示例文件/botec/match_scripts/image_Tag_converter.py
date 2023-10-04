#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import rospy
import tf
import math
from sensor_msgs.msg import Image
from ar_track_alvar_msgs.msg import AlvarMarkers
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


class ImgConverter():
    def __init__(self):
        self.bridge = CvBridge()
        self.sub_chest = rospy.Subscriber('/usb_cam_chest/image_raw', Image, self.cb_chest)
        # self.pub_chest_rotated = rospy.Publisher("/usb_cam/image_rotated", Image)
        self.img_chest = None

    def cb_chest(self, msg):
        cv2_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        self.img_chest = cv2_img

        # cv2_img_rot = np.rot90(cv2_img)
        # self.pub_chest_rotated.publish(self.bridge.cv2_to_imgmsg(cv2_img_rot, "bgr8"))

    def chest_image(self):
        return True, self.img_chest


class TagConverter():
    def __init__(self):
        # print('__init__')
        self.sub = rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.sub_cb)
        self.markers = []

    def sub_cb(self, msg):
        # print('sub_cb')
        markers_load = []
        time_sec = msg.header.stamp.secs
        # if len(msg.markers) == 0:
        #     print('msg.markers 为 空')
        for marker in msg.markers:
            pos = marker.pose.pose.position
            quat = marker.pose.pose.orientation

            # print(marker)

            rpy = tf.transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])  # 四元数转欧拉角
            rpy_arc = [0, 0, 0]
            for i in range(len(rpy)):   #弧度转角度
                rpy_arc[i] = rpy[i] / math.pi * 180

            # print(rpy_arc)
            # print("poseX:", pos.x, "poseY:", pos.y, "poseZ:", pos.z)
            # print("poseX--poseY--rpy_y:", pos.x, ",", pos.y, ",",rpy_arc[2])       # 测试标点
            if len(rpy_arc) == 0:
                print('rpy_arc 为 空')
            markers_load.append([marker.id, pos.x, pos.y, rpy_arc[2], time_sec])  # (id,x,y,z,  )

        # if len(markers_load) == 0:
        #     print('markers_load 为 空')
        self.markers = markers_load.copy()

    def get_markers(self):
        # print('get_markers')
        return self.markers

    def get_nearest_marker(self):
        '''
        返回最小id二维码
        '''
        # print('get_nearest_marker')
        min_id = 15
        min_idx = 0
        markers = []
        for i in range(20):
            time.sleep(0.01)
            markers += self.markers
            # if len(self.markers) == 0:
            #     print('self.markers 为 空')

        for index, m in enumerate(markers):
            if m[0] < min_id:  # 比较每个markers的第一值，即id
                min_idx = index
                min_id = m[0]
        if min_id == 15:
            return []
        else:
            return markers[min_idx]   #返回距离最近的ARTag信息


def main():
    try:
        rospy.init_node('image_listener')
        print('Node init')
        image_reader = ImgConverter()

        while True:
            rospy.spin()
            time.sleep(0.01)

    except rospy.ROSInterruptException:
        pass

# testing
if __name__ == '__main__':
    main()
