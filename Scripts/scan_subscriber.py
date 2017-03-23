#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Created by Abhi Ravikumar (abhi.ravikumar@protonmail.com)
# Graduate Students @ The University of Texas at San Antonio, TX U.S.A
# Research Students @ Autonomous Control & Engineering (ACE) Laboratory at UTSA
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#!/usr/bin/env python

import math
import rospy
from numpy import *
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

pub = None
min_distance = 0
current_distance = 0

x = 0
y = 0

def odomCB(msg):
    global x,y
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    return x

def rangeCB(msg):
    global i, pub, x, y, min_distance, current_distance
    dist_range=array(msg.ranges)
    Nans = isnan(dist_range)
    dist_range[Nans] = 20
    red_fov = dist_range[180:458] 
    if (i==1):
       writefile = open("Depthdata.csv","w")
       min_distance = min(red_fov)
       i += 1
    f = (x**2 + y**2)  #current_distance, f = root of (x^2 +y^2)
    print math.sqrt(f)   
    required_distance = min_distance - math.sqrt(f)  #current_distance
    print('required distance:', required_distance)
    if (required_distance > 0.4):
         print("above 0.4")
         cmd_vel = 0.15
    elif (required_distance <= 0.4):
         cmd_vel = 0
      #if min_distance is not None:
    twist_msg = Twist()
    twist_msg.linear.x = cmd_vel
    pub.publish(twist_msg)
    print("publishing")

def main():
    global i, min_distance, pub
    i = 1
    rospy.init_node('dist_range',anonymous=True)
    rospy.Subscriber("/odom", Odometry, odomCB)
    rospy.Subscriber("/scan", LaserScan, rangeCB)
    pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size = 10)
    rospy.spin()
    
if __name__ =='__main__':
    main()
