#!/usr/bin/python
import rospy
from custom_msg_python.msg import custom
from geometry_msgs.msg import TwistStamped
import math

msg_c = custom()
def callback(data):
 
    msg = TwistStamped()
    #rospy.loginfo("data is being received")
    x = data.x-320
    y = data.y -240
    z = data.z 
    
    Ex = (z/140)*(x/4)
    Ey = (z/140)*(y/4)
    Ez = z-0.2
    print(Ex,Ey,Ez)
    X.append(Ex)
    Y.append(Ey)
    Z.append(Ez)
    #print(X[0],Y[0],Z[0])
    c = 0.2
    epsilon = 0.8
    S = rospy.get_time()
    time.append(S)
    T = time[-1] -time[1]
    current_time.append(T)
    t =10
    Px = X[0] 
    Py = Y[0]
    Pz = Z[0]
    if T<10:
       X_t = (2*Px/t**3)*T**3 +(-3*Px/t**2)*T**2+Px
       #X_t = (0.002*X[0])*T**3 + (-0.03*X[0])*T**2 + X[0]
       trajectory_x.append(X_t)
       D_x = (trajectory_x[-1]-trajectory_x[-2])/(current_time[-1]-current_time[-2])
       V_x = -D_x + epsilon*math.tanh(c*(Ex-X_t))
        
       if V_x > 2:
          V_x = 0
       if V_x < -2:
          V_x = 0
       
       Y_t = (2*Py/t**3)*T**3+(-3*Py/t**2)*T**2+Py  
       #Y_t = (0.002*Y[0])*T**3 + (-0.03*Y[0])*T**2 + Y[0]
       trajectory_y.append(Y_t)
       D_y = (trajectory_y[-1]-trajectory_y[-2])/(current_time[-1]-current_time[-2])
       V_y = D_y - epsilon*math.tanh(c*(Ey-Y_t))
       
       if V_y > 2:
          V_y = 0
       if V_y < -2:
          V_y = 0

      
       
       #print(V_x, V_y, V_z)
    elif T>10:
        
        V_x =  epsilon*math.tanh(c*Ex)
        V_y = - epsilon*math.tanh(c*Ey)
        V_z = - epsilon*math.tanh(c*Ez)
        
        #print(V_x, V_y, V_z)
    t_z = 20
    if T<20:
       Z_t = (2*Pz/t_z**3)*T**3+(-3*Pz/t_z**2)*T**2+Pz
       #Z_t = (0.002*Z[0])*T**3 + (-0.03*Z[0])*T**2 + Z[0]
       trajectory_z.append(Z_t)
       D_z = (trajectory_z[-1]-trajectory_z[-2])/(current_time[-1]-current_time[-2])
       V_z = D_z - 0.4*math.tanh(0.3*(Ez-Z_t))
      

       if V_z > 2:
          V_z = 0
       if V_z < -2:
          V_z = 0
    elif T>20:
       V_z = - 0.3*math.tanh(0.5*Ez)
    print(V_x, V_y, V_z)
    
    msg_c = custom()
    msg_c.x = Ex
    msg_c.y = Ey
    msg_c.z = Ez
    msg.twist.linear.x = V_x
    msg.twist.linear.y = V_y
    msg.twist.linear.z = V_z
    pub.publish(msg)
    pubg.publish(msg_c)
    
    
       
       
       
    
    




if  __name__ == "__main__":
    rospy.init_node("subscriber",anonymous=True)
    initial_time=rospy.get_time()
    global time,trajectory_x,trajectory_y,trajectory_z,current_time,X,Y,Z
    
    time=[initial_time]
    X = []
    Y = []
    Z = []
    trajectory_x=[0]
    trajectory_y=[0]
    trajectory_z=[0]
    current_time=[0.0001]
    sub = rospy.Subscriber('obj_coordinate',custom, callback)
    pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=2)
    pubg = rospy.Publisher('error_trejectory', custom, queue_size=2)
 
    rate=rospy.Rate(10)
  
    rospy.spin()
