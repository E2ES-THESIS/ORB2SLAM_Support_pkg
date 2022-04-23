#!/usr/bin/env python
import rospy 
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
class camera_conv_bw_Node:
    def __init__(self):
        rospy.init_node("ros_node")
        rospy.loginfo("Starting camera_conv_bw_Node.")
        self.bridge_object = CvBridge()
        self.img = Image()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.image_callback)
        self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size=10)
        

    def image_callback(self,data):
        self.img = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        bw_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.image_pub.publish(self.bridge_object.cv2_to_imgmsg(bw_img, "8UC1"))
        cv2.imshow("org",self.img)
        cv2.imshow("bw",bw_img)
        cv2.waitKey(1)

if __name__ == "__main__":
    ros_node = camera_conv_bw_Node()
    rospy.spin()

