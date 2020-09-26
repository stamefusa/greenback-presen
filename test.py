# -*- coding: utf-8 -*-

import cv2
import numpy as np

# 最終的に表示する画像サイズ
width  = 1280
height = 720

# キャプチャしたカメラ画像のリサイズ
ratio = 20 # 背景に対して何%のサイズにするか
r_width = int(width*ratio/100)
r_height = int(height*ratio/100)

# カメラ画像の表示位置オフセット
offset_y = 80

# カメラ画像のグリーンバック以外の余白
ratio_l = 0.26 # 左
ratio_r = 0.4 # 右
ratio_u = 0.15 # 上

#chroma key color band HSV data
lower_color = np.array([30, 35, 35])
upper_color = np.array([100, 255, 255])
#OpenCV HSV H:0-180,S:0-255,V:0-255
#But populer HSV H:0-360 so I use [0..360]/2

#capture device open
cap = cv2.VideoCapture(1)   #for object

front = cv2.imread('./front.jpg')
bak = cv2.imread('./back.jpg')
#bak = cv2.imread('./pink.jpg')
back = cv2.resize(bak, dsize=(width, height))

while(1):
    # Take each frame
    ret, frame = cap.read()

    frame = cv2.resize(frame, dsize=(r_width, r_height))
    front[(height-r_height-offset_y):(height-offset_y), int((width-r_width)/2):int((width+r_width)/2)] = frame

    # カメラ画像の範囲外を緑で塗る
    front[:, int((width-r_width)/2):int((width-r_width)/2+ratio_l*r_width)] = [100, 160, 130]
    front[:, int((width+r_width)/2-ratio_r*r_width):width] = [100, 160, 130]
    front[(height-r_height-offset_y):int(height-r_height+ratio_u*r_height-offset_y), :] = [100, 160, 130]


    # Convert BGR to HSV
    hsv = cv2.cvtColor(front, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)

    inv_mask = cv2.bitwise_not(mask)

    # Bitwise-AND mask,inv_mask and original image
    res1 = cv2.bitwise_and(front, front, mask=inv_mask)
    res2 = cv2.bitwise_and(back, back, mask=mask)

    #compsiting
    disp = cv2.bitwise_or(res1, res2, mask)

    ##show
    cv2.imshow('front', front)
    cv2.imshow('disp', disp)
    #cv2.imshow('back', back)

    # When hit the ESC-key go to exit
    k = cv2.waitKey(60) 
    if k == 27:
        break

#close all windows    
cv2.destroyAllWindows()
