#!/usr/bin/python
import rospy
import message_filters
from custom_msg_python.msg import custom
from std_msgs.msg import Float64
msg = custom()

def sub():
    xypos = message_filters.Subscriber('center_coordinate', custom)
    zpos = message_filters.Subscriber('/mavros/global_position/rel_alt',  Float64)

    merge = message_filters.ApproximateTimeSynchronizer([xypos,zpos],10,0.1,allow_headerless=True)
    merge.registerCallback(callback)
    rospy.spin()
    
def callback(custom_message,z_dummy_coordinate):
    pub = rospy.Publisher('obj_coordinate',custom, queue_size=10)
    msg = custom()
    msg.x = custom_message.x
    msg.y = custom_message.y
    msg.z = z_dummy_coordinate.data
    #msg.theta = custom_message.custom.data.theta
    print(msg.x,msg.y,msg.z)
    pub.publish(msg)
    rospy.sleep(0)
if __name__=='__main__':
   rospy.init_node('obj_cordi', anonymous = True)
   try:
      sub()
   except rospy.ROSInterruptException:
      pass
