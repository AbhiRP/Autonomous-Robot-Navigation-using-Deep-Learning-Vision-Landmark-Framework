#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Created by Abhi Ravikumar (abhi.ravikumar@protonmail.com)
# Graduate Student @ The University of Texas at San Antonio, TX U.S.A
# Research Assistant @ Autonomous Control & Engineering (ACE) Laboratory at UTSA
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''=================================================================================
Python scrpit for 
1) Listing all recognized objects by the Inception V3 Image Classification engine.
2) Accepting an input from user.
3) Scaning the csv file for the position of the target.
4) Orienting the robot towards the target.
================================================================================='''


#!/usr/bin/env python

import numpy as np
import pandas as pd
import scipy
import math
import string
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Twist


pub = None
yaw = None
angle_towards_object = None
error = None

def yawCB(msg):
    global yaw, angle_towards_object
    yaw = msg.z
    if angle_towards_object is not None:
       cmd_angular_v = target(angle_towards_object)
       twist_msg = Twist()
       twist_msg.angular.z = cmd_angular_v
       pub.publish(twist_msg)
    #print(angle_towards_object)
    
def dataread():
    data = pd.read_csv("NewFile.csv")
    location, objects = np.array(data.ix[:,0]), np.array(data.ix[:,1])
    numobjects = len(objects)
    print(objects)
    print(numobjects)
    req_item = raw_input("What is the Item?\n")
    temp = 0
    numfound = 0
    for i in [i for i,x in enumerate(objects) if x ==req_item]:
       temp += location[i]
       numfound += 1
    avg_location = temp/numfound
    print(avg_location)
    return avg_location

def target(required_angle):
    global error, yaw
    error = required_angle - yaw
    if (error >=0.11):
       cmd_vel = 0.25
    elif (error <= -0.11):
       cmd_vel = -0.25
    elif (error < 0.11 and error >= -0.11):
       cmd_vel = 0
    print(error)
    return cmd_vel


def main():
    global yaw, pub, angle_towards_object, error
    rospy.init_node('test', anonymous=True)
    angle_towards_object = dataread()
    rospy.Subscriber("/rpy_angles", Vector3, yawCB)
    pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size = 10)
    rospy.spin()

if __name__ == '__main__':
    main()
