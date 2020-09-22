#!/usr/local/bin/python3

import cv2
import numpy as np

#capture frame size
width  = 1320
height = 960

#chroma key color band HSV data
lower_color = np.array([60,55,55])
upper_color = np.array([180,255,255])
#OpenCV HSV H:0-180,S:0-255,V:0-255
#But populer HSV H:0-360 so I use [0..360]/2

#capture device open
cap = cv2.VideoCapture(1)   #for object
#
#bak = cv2.VideoCapture(0)   #for background
#bak = cv2.imread('./3810600_l.jpg')
bak = cv2.imread('./pink.jpg')
back = cv2.resize(bak, dsize=(width, height))

while(1):
    # Take each frame
    ret, frame = cap.read()
    #ret, back = bak.read()

    frame = cv2.resize(frame, dsize=(width, height))
    #back = cv2.resize(back, dsize=(width, height))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    inv_mask = cv2.bitwise_not(mask)

    # Bitwise-AND mask,inv_mask and original image
    res1 = cv2.bitwise_and(frame,frame,mask=inv_mask)
    res2 = cv2.bitwise_and(back,back,mask=mask)

    #compsiting
    disp = cv2.bitwise_or(res1,res2,mask)

    ##show
    cv2.imshow('frame',frame)
    cv2.imshow('disp',disp)
    #cv2.imshow('back',back)

    # When hit the ESC-key go to exit
    k = cv2.waitKey(60) 
    if k == 27:
        break

#close all windows    
cv2.destroyAllWindows()
