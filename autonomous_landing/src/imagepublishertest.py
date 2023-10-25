#!/usr/bin/python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

capt = cv2.VideoCapture(0)
bridge = CvBridge()

rospy.init_node("imag_capture_obj")
pub = rospy.Publisher("img_bgr_publish", Image, queue_size=1)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
	ret,frame = capt.read()
	if not ret:
	   break
      cv2.imshow("frame",frame)
	msg = bridge.cv2_to_imgmsg(frame,"bgr8")
	pub.publish(msg)

	if cv2.waitKey(1) & 0XFF==ord('q'):
	   break
	if rospy.is_shutdown():
	   capt.release()



