#!/usr/bin/python
import rospy
import cv2
import numpy as np
from custom_msg_python.msg import custom
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import imutils
from std_msgs.msg import Float64

bridge = CvBridge()
#def empty(a):
 #   pass
def empty(a):
    pass
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("Hue_min","HSV",0,179,empty)
cv2.createTrackbar("Hue_max","HSV",179,179,empty)
cv2.createTrackbar("sat_min","HSV",0,255,empty)
cv2.createTrackbar("sat_max","HSV",255,255,empty)
cv2.createTrackbar("Value_min","HSV",0,255,empty)
cv2.createTrackbar("Value_max","HSV",255,255,empty)

def call(frame):
  
  img = bridge.imgmsg_to_cv2(frame, "bgr8")
  
  img = cv2.resize(img,(640,480))
  dimension = img.shape
  #print(dimension)
  imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  
  h_max = cv2.getTrackbarPos("Hue_max","HSV")
  h_min = cv2.getTrackbarPos("Hue_min","HSV")
  s_min = cv2.getTrackbarPos("sat_min","HSV")
  s_max = cv2.getTrackbarPos("sat_max","HSV")
  v_min = cv2.getTrackbarPos("Value_min","HSV")
  v_max = cv2.getTrackbarPos("Value_max","HSV")
  #cv2.imshow("imgHSV",imgHSV)
  lower = np.array([5,0,0])
  upper = np.array([179,255,255])
  #lower = np.array([h_min,s_min,v_min])
  #upper = np.array([h_max,s_max,v_max])
  mask = cv2.inRange(imgHSV,lower,upper)
  img_cont = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  img_cont = imutils.grab_contours(img_cont)
  result = cv2.bitwise_and(img,img, mask = mask)
  cv2.imshow('Mask', mask)

  for c in img_cont:
        
       area = cv2.contourArea(c)
       if  area < 100000 and area > 4:
           cv2.drawContours(img,[c],-1,(0,255,0),3)
           M = cv2.moments(c)
      
           cx = int(M["m10"]/M["m00"])
           cy = int(M["m01"]/M["m00"])
           cv2.circle(img, (cx,cy), 7,(255,255,255),-1)
           cv2.imshow("contour",img)
           print("centroid",cx,cy)
           msg = custom()
           msg.x = cx
           msg.y = cy
           #msg.z = 2
           pubg.publish(msg)
       
           print("area is ...",area)
  cv2.imshow('Result',img)
  
  #num = 2
  #print(num)
  cv2.waitKey(1)
#def z_cor():
   #z_cordinate = data.data
   #msg.z = z_cordinate
   #pubg.publish(msg)
    

if __name__=="__main__":
   rospy.init_node('obj_pub')
   sub = rospy.Subscriber('/webcam/image_raw',Image, call)
   #sub2 = rospy.Subscriber('/mavros/global_position/rel_alt',Float64, z_cor)
   pubg = rospy.Publisher('center_coordinate', custom, queue_size=10)
   rate = rospy.Rate(10)
   rospy.spin() 
