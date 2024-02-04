#!/usr/bin/python3

''' 
Code to detect and follow a color 
    
Run the color_detection launch commands before this file 

Execute with python3 color_detection.py 

Complete this template and the template files color_image and velocity
'''

# Import libraries
########################################################################
import cv2
import numpy as np 
import rospy
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from color_image import show_image, get_color_range, detect_color, get_max_contour
from velocity import get_velocity


# Variables 
########################################################################
bridge = CvBridge()
min_detection = 1000  # Minimum area for considering a detection


# Image callback -> it is called when the topic receives information
################################################################
def image_callback(msg):
    
    rospy.loginfo("Image received")

    # Get image and publisher 
    ##########################################

    # Convert your ros image message to opencv using bridge
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)
        return

    # Show image using show_image function
    show_image(cv_image, "Original Image")

    # Get half width of the image 
    height, width, _ = cv_image.shape
    half_width = width // 2

    # Create velocity publisher and variable of velocity
    velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    velocity = Twist()
    
    # Do color detection 
    ##########################################

    # Get color range using get_color_range from color_image.py
    color_range = get_color_range()  # Assuming you have a function to get color range

    # Get color mask using detect_color from color_image.py
    color_mask = detect_color(cv_image, color_range)

    # Show mask 
    show_image(color_mask, "Color Mask")

    # Find contours and get max area using get_max_contours from color_image.py 
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour, area = get_max_contour(contours)
    print("Maximum area: ", area)

    # Get robot speed     
    ##########################################

    # If the area of the detected color is big enough
    if area > min_detection:
        print("Cylinder detected")

        # Draw contour and center of the detection and show image 
        cv2.drawContours(cv_image, [max_contour], -1, (0, 255, 0), 3)
        M = cv2.moments(max_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(cv_image, (cx, cy), 7, (255, 0, 0), -1)
        cv2.putText(cv_image, "Center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        show_image(cv_image, "Detection")

        # Gets the color speed and direction depending on the color detection using get_velocity from velocity.py
        velocity = get_velocity(cx, half_width)  # Assuming you have a function to calculate velocity
            
    # If the area of the detected color is not big enough, the robot spins 
    else:
        print("Looking for color: spinning")
        # Assuming you want the robot to spin in place, you can set angular velocity
        velocity.angular.z = 0.5  # Example angular velocity

    # Publish velocity
    velocity_pub.publish(velocity)


# Init node and subscribe to image topic 
################################################################
def main():
    # Init node 'color_detection'
    rospy.init_node('color_detection', anonymous=True)

    # Subscribe to image topic and add callback + spin
    rospy.Subscriber('/camera/image_raw', Image, image_callback)
    rospy.spin()
    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
