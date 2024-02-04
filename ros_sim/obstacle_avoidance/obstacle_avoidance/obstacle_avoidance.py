#!/usr/bin/python3

''' 
Code to develop an algorithm to avoid obstacles
    
Run the color_detection launch commands before this file 

Execute with python3 obstacle_avoidance.py 

Complete this template and the template file obstacle_functions.py 
'''

import cv2
import numpy as np 
import rospy
import numpy as np 
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan

from obstacle_functions import get_all_section_values, get_velocity


# Variables
turning_left = False

# Laser callback -> it is called when the topic receives information
def laser_callback(msg):
    global turning_left

    # Create velocity publisher and velocity variable
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel = Twist()

    # Read laser scan data and get section values
    all_sides, all_sides_mean = get_all_section_values(msg)

    # Sort laser scan section indexes using the means from clearer sections to less clear sections
    clearer_path_indexes = np.argsort(all_sides_mean)[::-1]

    # Extract the 3 most clearer sections
    three_clearest_paths = clearer_path_indexes[:3]

    # Get robot velocity depending on laser values
    vel, turning_left = get_velocity(all_sides_mean, three_clearest_paths, turning_left, vel)

    # Publish velocity
    vel_pub.publish(vel)

# Init node and subscribe to laser scan topic
def main():
    rospy.init_node('obstacle_avoidance', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, laser_callback)
    rospy.spin()

if __name__ == '__main__':
    main()