#!/usr/bin/python3

'''
FUNCTIONS FOR OBSTACLE AVOIDANCE CODE
'''

import numpy as np

# Gets all the values for each section of the laser scan and its mean value 
def get_all_section_values(msg):

    # We create the list where we will save the values of each sections
    all_sides = []
    all_sides_mean = []
    
    # Read center laser scan data 
    side = np.array([msg.ranges[-15:], msg.ranges[:15]]).flatten()
    side = side[~np.isnan(side) & ~np.isinf(side)]
    all_sides.append(side)
    all_sides_mean.append(np.mean(side))
   
	
    # We add the center section values and the mean
    all_sides.append(side)
    all_sides_mean.append(np.mean(side))
   
   
    # Add laser scan data every 30 degrees 
    for d in range(15,345,30):
        side = np.array(msg.ranges[d:d+30])
        side = side[~np.isnan(side) & ~np.isinf(side)]
        all_sides.append(side)
        all_sides_mean.append(np.mean(side))
    
    print("\n",all_sides_mean)

    return all_sides, all_sides_mean


# Gets the robot velocity based on the clearest paths 
##############################################################################################################
# Parameters:                                                                                                #
# - all_sides_mean: mean values of each section                                                              #
# - three_clearest_paths: the indexes of the  three sections with higher means (obstacles are more far away) #
# - turning_left: it will be True if the robot is turning left, and False otherwise                          #
# - vel: velocity Twist vector                                                                               #
##############################################################################################################
# The front directions are saved at the 0, 1 and 11 indexes                                                  #
##############################################################################################################

def get_velocity(all_sides_mean, three_clearest_paths, turning_left, vel): 
	
    # Get the index of the clearest path 
    clearest_path = np.argmax(all_sides_mean)
    print(clearest_path)

    # If the mean value of the front section is less than 1.0
    if(all_sides_mean[0] < 1.0 or all_sides_mean[1] < 1.0 or all_sides_mean[-1] < 1.0):
        # Check if any of the three front sections is not in the three_clearest_paths
        if(0 not in three_clearest_paths or 1 not in three_clearest_paths or 11 not in three_clearest_paths):
            # If the clearest_path is between 1-5 indexes (included) or we are already turning left --> Turn left
            if(clearest_path > 0 and clearest_path < 6 or turning_left):
                print("Turn left")
                #vel.linear.x = 0.0
                vel.angular.z = 0.3  # Update turning_left to True
                turning_left = True  # Turn to left
            # If the clearest_path is 0 or >5 or we are not turning to left --> Turn right
            else: 
                print("Turn right")
                #vel.linear.x = 0.0
                vel.angular.z = -0.3  # Update turning_left to False
                turning_left = False  # Turn to right
        else:
            # Go straight to avoid being trapped spinning 
            print("Go straight 1")
            vel.linear.x = 0.2
            #vel.angular.z = 0.0  # Update turning_left to False
            turning_left = False  # Go straight
    # If none of the front directions are less than 1.0 (clear path ahead) -> Go straight
    else:
        print("Go straight 2")
        vel.linear.x = 0.3
        #vel.angular.z = 0.0  # Update turning_left to False
        turning_left = False  # Go straight


    return vel, turning_left