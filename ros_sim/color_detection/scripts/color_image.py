#!/usr/bin/python3

'''
FUNCTIONS FOR COLOR DETECTION CODE
'''

import cv2 

# Resize and show image 
def show_image(img, window_name): 
    img_res = cv2.resize(img, None, fx=0.3, fy=0.3)
    cv2.imshow(window_name, img_res)
    cv2.waitKey(1)


# Get color limits
def get_color_range(color):
    
    # Complete only for the color you want to detect 

    if color == 'red':
        lower_range = (170, 50, 50)
        upper_range = (10, 255, 255)
 
    # elif color == 'green':
    #     lower_range = (40, 50, 50)
    #     upper_range = (90, 255, 255)

    elif color == 'blue':
        lower_range = (100, 0, 0)
        upper_range = (150, 255, 255)

    else:  # Yellow 
        lower_range = (20, 100, 100)
        upper_range = (30, 255, 255)
    
    return lower_range, upper_range



# Detects the color 
def detect_color(img, lower_range, upper_range):

    # Perform a Gaussian filter 
    image_gauss = cv2.GaussianBlur(img, (5,5), 1)

    # Convert gauss image to HSV
    hsv_img = cv2.cvtColor(image_gauss, cv2.COLOR_BGR2HSV)

    # Get color mask
    mask = cv2.inRange(hsv_img, lower_range, upper_range)

    # Define rectangular kernel 25x25
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,25))

    # Apply openning to mask 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    return mask



# Get maximum contour, area and its center 
def get_max_contour(mask): 

    contour_max = []
    area_max = 0
    center = (0,0)

    
    # Find contours
    ret, gray_thresh = cv2.threshold(mask, 0, 254, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(gray_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # For each contour
    for cont in contours:
    
        # Get area of the contour 
        area = cv2.contourArea(cont)

        # If area is bigger than area_max 
        if area > area_max:
            # Update area max value 
            area_max = area

            # Update contour_max value
            contour_max = cont

            # Get center of the contour using cv2.moments
            M = cv2.moments(cont)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                # Set default center if moments are zero
                cx, cy = 0, 0

        center = (cx,cy)



    return contour_max, area_max, center