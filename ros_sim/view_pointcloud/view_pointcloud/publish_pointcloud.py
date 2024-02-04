#!/usr/bin/python3

''' 
Code to publish the pointcloud information to the topic /my_pointcloud 
    
Run the navigation commands before this file 

Execute with python3 publish_pointcloud.py 

Change your pointcloud path 
'''


import rospy
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
import std_msgs.msg
import open3d as o3d
import numpy as np 


# Function to publish the point cloud
def publisher():

    # Create pointcloud publisher
    pointcloud_publisher = rospy.Publisher("/my_pointcloud", PointCloud, queue_size=10)

    # Init node 
    rospy.init_node('pointcloud_node')
    rate = rospy.Rate(10) # Rate to publish 10hz

    # Read pointcloud
    pcd = o3d.io.read_point_cloud('/home/esther/mymaps/cloud.ply>') # CHANGE TO YOUR PATH!!
    
    # Gets the xyz points from the pointcloud  
    xyz_points = np.asarray(pcd.points)

    # Save the points in the required format
    my_pointcloud = []
    for point in xyz_points:
       my_pointcloud.append(Point32(point[0],point[1],point[2]))
    
    
    # Give time to roscore to make the connections
    rospy.sleep(1.)
      
    # While the node is active 
    while not rospy.is_shutdown():
      
      # Declaring pointcloud
      pointcloud = PointCloud()
      
      # Adding some pointcloud information to the header
      header = std_msgs.msg.Header()
      header.stamp = rospy.Time.now()
      header.frame_id = 'map'
      pointcloud.header = header
      
      # Add the points 
      pointcloud.points = my_pointcloud
      
      # Publish to the topic  
      rospy.loginfo("Publishing pointcloud to /my_pointcloud topic !")
      pointcloud_publisher.publish(pointcloud)



if __name__ == '__main__':
    publisher()
    