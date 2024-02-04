#!/usr/bin/python3

''' 
Code to take images from the robot camera every x seconds
    
Run the color_detection commands before this file 

Execute with python3 take_images.py 

Change your image saving path 
'''

# Import libraries
########################################################################
import cv2
import numpy as np 
import rospy
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time 


# Variables 
########################################################################
bridge = CvBridge()
counter = 0
last_time = time.time()


# Show image 
################################################################
def show_image(img, window_name): 
    img_res = cv2.resize(img, None, fx=0.3, fy=0.3)
    cv2.imshow(window_name, img_res)
    cv2.waitKey(1)


# Image callback 
################################################################
def image_callback(msg):
    global counter 
    global last_time 
    
    # Convert your ROS Image message to OpenCV2
    img = bridge.imgmsg_to_cv2(msg, "bgr8")
    #show_image(img)

    # Gets actual time 
    actual_time = time.time()

    # Saves an image every 3.5 seconds
    if(actual_time-last_time > 3.5):  
       rospy.loginfo("Saving image")
       filename = "/home/esther/images_ros/image_{0}.jpg".format(counter) # CHANGE TO YOUR PATH!
       cv2.imwrite(filename, img)
       counter = counter + 1
       last_time = actual_time



# Init node and suscribe to image topic 
################################################################
def main():
    rospy.init_node('image_saver')
    rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)
    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    
    
    