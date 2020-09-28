# -*- coding: utf-8 -*-

import cv2
import numpy as np

# 最終的に表示する画像サイズ
width  = 1280
height = 720

# キャプチャしたカメラ画像のリサイズ
ratio = 10 # 背景に対して何%のサイズにするか(40%がちょうどいい)
r_width = int(width*ratio/100)
r_height = int(height*ratio/100)

# カメラ画像の表示位置オフセット
offset_y = 40 # 下からのオフセット
offset_x = 0 # 左からのオフセット
if int((width+r_width)/2+offset_x) > width:
    offset_x = int((width-r_width)/2)

# カメラ画像のグリーンバック以外の余白
ratio_l = 0.2 # 左
ratio_r = 0.4 # 右
ratio_u = 0.15 # 上

# chroma key color band HSV data
lower_color = np.array([30, 35, 35])
upper_color = np.array([100, 255, 255])

# capture device open
cap = cv2.VideoCapture(1)   #for object

# 画像読み込み
front = cv2.resize(cv2.imread('./front.jpg'), dsize=(width, height))
#front_z = cv2.resize(cv2.imread('./front.jpg'), dsize=(width, height))
#back = cv2.resize(cv2.imread('./pink.jpg'), dsize=(width, height))
back = cv2.resize(cv2.imread('./back.jpg'), dsize=(width, height))
zoom = cv2.resize(cv2.imread('./zoom.jpg'), dsize=(width, height))

# プレゼン資料読み込み
p_width = 960
p_height = 540
p_offset = 50 # 上からのオフセット
page = cv2.resize(cv2.imread('./page4.jpg'), dsize=(p_width, p_height))
back[p_offset:p_height+p_offset, int((width-p_width)/2):int((width+p_width)/2)] = page

while(1):
    ret, org_frame = cap.read()

    frame = cv2.resize(org_frame, dsize=(r_width, r_height))
    front[(height-r_height-offset_y):(height-offset_y), int((width-r_width)/2+offset_x):int((width+r_width)/2+offset_x)] = frame
    
    frame_z = cv2.resize(org_frame, dsize=(width, height))
    front_z = cv2.resize(frame_z[90:270, 350:670], dsize=(width, height))

    # カメラ画像の範囲外を緑で塗る
    front[:, int((width-r_width)/2):int((width-r_width)/2+ratio_l*r_width+offset_x)] = [100, 160, 130]
    front[:, int((width+r_width)/2-ratio_r*r_width)+offset_x:width] = [100, 160, 130]
    front[(height-r_height-offset_y):int(height-r_height+ratio_u*r_height-offset_y), :] = [100, 160, 130]

    # ここからズーム画像用の処理
    # Convert BGR to HSV
    hsv_z = cv2.cvtColor(front_z, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask_z = cv2.inRange(hsv_z, lower_color, upper_color)

    inv_mask_z = cv2.bitwise_not(mask_z)

    # Bitwise-AND mask,inv_mask and original image
    res1_z = cv2.bitwise_and(front_z, front_z, mask=inv_mask_z)
    res2_z = cv2.bitwise_and(zoom, zoom, mask=mask_z)

    #compsiting
    disp_z = cv2.bitwise_or(res1_z, res2_z, mask_z)

    # ここからメイン画像の処理
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

    # ズーム画像をメイン画像に重畳
    disp[100:100+270, 700:700+480] = cv2.resize(disp_z, dsize = (480, 270))

    ##show
    cv2.imshow('front', front)
    cv2.imshow('disp', disp)
    #cv2.imshow('disp_z', disp_z)
    #cv2.imshow('back', back)

    # When hit the ESC-key go to exit
    k = cv2.waitKey(60) 
    if k == 27:
        break

#close all windows    
cv2.destroyAllWindows()
