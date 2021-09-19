#Before runing install (pip install opencv-python)
import cv2
import time
import numpy as np

# To save the output in a file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

cam = cv2.VideoCapture(0)
time.sleep(2)
bg = 0

#Capturing background
for i in range(60):
    ret, bg = cam.read()

bg = np.flip(bg, axis = 1)

#Continuously reading/capturing the frames to replace any colors in that
while(cam.isOpened()):
    ret, img = cam.read()
    if not ret:
        break

    img = np.flip(img, axis = 1)

    #Converting the images from BGR to HSV(HUE - The number which indicated the color, 0-RED, 120-GREEN, 240-BLUE)
    #Saturation - The purity or intensity of color, Value - The brightness of the color
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Picking the range of light red color
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    #Picking the pices of light shade of red from the image
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    
    #Picking the range of brighter red color
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])

    #Picking the pices of bright shade of red from the image
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    #Open and expand the image where there are red colors of the image
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    #Selecting only the part that does not have red color
    mask_2 = cv2.bitwise_not(mask_1)

    #This is the part of the images without red color
    result1 = cv2.bitwise_and(img, img, mask = mask_2)

    #This is the part of the background image which are in the position of red patches
    result2 = cv2.bitwise_and(bg, bg, mask = mask_1)
    #Generating the final image by merging the both results by merging the patches from backgrond with foreground hole image
    final_output = cv2.addWeighted(result1, 1, result2, 1, 0)
    output_file.write(final_output)
    cv2.imshow('MAGIC', final_output)
    cv2.waitKey(1)
    
cam.release()
output.release()
cv2.destroyAllWindows()