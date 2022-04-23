#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

class Camera_Webcam(object):

	def __init__(self):
		self.orb = cv2.ORB_create(nfeatures=1500)
		self.bridge_object = CvBridge()
		self.image_sub = rospy.Subscriber("/image_in",Image,self.camera_callback)

	def camera_callback(self,data):
		try:
			cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
		except CvBridgeError as e:
			print(e)

		img = cv_image
		keypoints_orb, descriptors = self.orb.detectAndCompute(img, None)
		img = cv2.drawKeypoints(img, keypoints_orb, None)
		cv2.imshow("Original", cv_image)
		cv2.imshow("Orb", img)
		fourcc = cv2.VideoWriter_fourcc(*'MJPG')
		self.video_writer = cv2.VideoWriter("1.avi", fourcc, 20, (320,240))
		cv2.waitKey(1)
	def clean_up(self):
		cv2.destroyAllWindows()


def main():
	rospy.init_node('feature_detection_node', anonymous=True)
	cam_object = Camera_Webcam()
	rate = rospy.Rate(5)
	ctrl_c = False
	def shutdownhook():
	# works better than the rospy.is_shut_down()
		cam_object.clean_up()
		rospy.loginfo("shutdown time!")
		ctrl_c = True
	rospy.on_shutdown(shutdownhook)
	while not ctrl_c:
		rate.sleep()
if __name__ == '__main__':
	main()
