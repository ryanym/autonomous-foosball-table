'''
by Chenhe, Roland
November 14, 2015
ball tracking and path prediction
ball path prediction only does on reflection on the long side
'''

import numpy as np
import cv2
import time

#constants
CAM_ID = 0
CAM_WIDTH = 320
CAM_HEIGHT = 240
CAM_FPS = 90

'''
The Edge of the playfield, use for cut capture image
new coordinte after cut
0,0                         0,EDGE_Y_MAX-EDGE_Y_MIN-1
EDGE_X_MAX-EDGE_X_MIN-1,0     EDGE_X_MAX-EDGE_X_MIN-1,EDGE_Y_MAX-EDGE_Y_MIN-1
'''
EDGE_X_MIN = 24
EDGE_X_MAX = 300
EDGE_Y_MIN = 22
EDGE_Y_MAX = 216

FIELD_L = 410 # mm
FIELD_W = 290 # mm
FIELD_L_PIXEL = EDGE_X_MAX - EDGE_X_MIN
FIELD_W_PIXEL = EDGE_Y_MAX - EDGE_Y_MIN

#BALL radiues in pixel
BALL_R = 14 #mm
BALL_R_MIN = 4
BALL_R_MAX = 10
BALL_R_PIXEL = int(BALL_R * FIELD_L_PIXEL / FIELD_L )
#Ball center moving area
BALL_X_MAX = FIELD_L_PIXEL - BALL_R_PIXEL -1
BALL_Y_MAX = FIELD_W_PIXEL - BALL_R_PIXEL - 1
BALL_X_MIN = BALL_R_PIXEL
BALL_Y_MIN = BALL_R_PIXEL

#print 1.0*FIELD_L_PIXEL / FIELD_L
#print 1.0*FIELD_W_PIXEL / FIELD_W

#BALL color
hsv = None
LOWER_H = 92
LOWER_S = 112
LOWER_V = 162
UPPER_H = 116
UPPER_S = 183
UPPER_V = 236

ERROR_FILTER = np.ones((2,2),np.uint8)

def nothing(x):
    pass

def find_ball_path(ball_cur,ball_pre):
    path = []
    ball_tar = [None] * 2
    ball_diff_x = ball_cur[0] - ball_pre[0]
    ball_diff_y = ball_cur[1] - ball_pre[1]

    if ball_diff_x > 0:
        ball_tar[0]  = BALL_X_MAX*1.0
    elif ball_diff_x == 0:
        ball_tar[0]  = ball_cur[0]
    elif ball_diff_x  < 0:
        ball_tar[0]  = BALL_X_MIN*1.0

    if ball_diff_y == 0:
        ball_tar[1]  = ball_cur[1]
        path.append((ball_cur,ball_tar))
    elif ball_diff_y  > 0:
        ball_col = [None] * 2
        if(ball_diff_x==0):
            ball_tar[1]  = BALL_Y_MAX
        else:
            ball_tar[1]  = ball_cur[0] + (ball_tar[0] - ball_cur[0])/ball_diff_x*ball_diff_y
        if ball_tar[1] > BALL_Y_MAX:
            ball_col[0] = ball_cur[0]+(BALL_Y_MAX-ball_cur[1])/ball_diff_y*ball_diff_x
            ball_col[1] = BALL_Y_MAX;
            ball_tar[1] = BALL_Y_MAX * 2 - ball_tar[1];
            path.append((ball_cur,ball_col))
            path.append((ball_col,ball_tar))
        else:
            path.append((ball_cur,ball_tar))

    elif ball_diff_y  < 0:
        ball_col = [None] * 2
        if(ball_diff_x==0):
            ball_tar[1]  = BALL_Y_MIN
        else:
            ball_tar[1]  = ball_cur[0] + (ball_tar[0] - ball_cur[0])/ball_diff_x*ball_diff_y
        if ball_tar[1] < BALL_Y_MIN:
            ball_col[0] = ball_cur[0]+(BALL_Y_MIN-ball_cur[1])/ball_diff_y*ball_diff_x
            ball_col[1] = BALL_Y_MIN;
            ball_tar[1] = BALL_Y_MIN * 2 - ball_tar[1];
            path.append((ball_cur,ball_col))
            path.append((ball_col,ball_tar))
        else:
            path.append((ball_cur,ball_tar))
    return path

def center_ftoi(center):
    return (int(center[0]),int(center[1]))


#set up campture
cap = cv2.VideoCapture(CAM_ID)
cap.set(3,CAM_WIDTH)
cap.set(4,CAM_HEIGHT)
cap.set(5,CAM_FPS)
#Filter
lowerb = np.array([LOWER_H,LOWER_S,LOWER_V])
upperb = np.array([UPPER_H,UPPER_S,UPPER_V])
kernel = np.ones((3,3),np.float32)/9

ball_pre = (-1,-1)
ball_cur = (-1,-1)

while(True):

    ret, frame = cap.read()
    frame_field = frame[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]
    dst = cv2.filter2D(frame_field,-1,kernel)
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    dest_image = cv2.inRange(hsv, lowerb, upperb)
    #reduce noise
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER,1)
    
    cv2.line(frame_field,(BALL_X_MIN,BALL_Y_MIN),(BALL_X_MAX,BALL_Y_MIN),(0,255,0),2,8,0)
    cv2.line(frame_field,(BALL_X_MIN,BALL_Y_MAX),(BALL_X_MAX,BALL_Y_MAX),(0,255,0),2,8,0)
    
    cv2.imshow("Binary Image",dilate)

    a,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    ball_found = False
    ball_radius_max = 4
    ball_center = (-1,-1)
    if len(contours) >0:
        for cnt in contours:
            (x,y),tmp_radius = cv2.minEnclosingCircle(cnt)
            if tmp_radius >BALL_R_MIN and tmp_radius <BALL_R_MAX:
                ball_found = True
                if tmp_radius > ball_radius_max:
                    ball_radius_max = tmp_radius
                    ball_cur = (x,y)
        if ball_found == False:
            print 'Ball not found'
            ball_pre = (-1,-1)
            ball_cur = (-1,-1)
        else:
            if ball_pre[0] >0 and ball_cur[0] >0:
                ball_path = find_ball_path(ball_cur,ball_pre)
                print ball_path
                for line in ball_path:
                    cv2.line(frame_field,center_ftoi(line[0]),center_ftoi(line[1]),(0,255,0),2,8,0)
                #cv2.line(frame,center_ftoi(ball_cur),center_ftoi((ball_cur[0]+(ball_cur[0]-ball_pre[0])*40,ball_cur[1]+(ball_cur[1]-ball_pre[1])*40)),(0,255,0),2,8,0)
            print 'preBall ',center_ftoi(ball_pre),'currentBall ',center_ftoi(ball_cur)
            ball_pre = ball_cur
            cv2.circle(frame_field,center_ftoi(ball_cur),int(tmp_radius),(0,255,0),2)
    else:
        print 'undetected'

    cv2.imshow('frame',frame)
    cv2.imshow('field',frame_field)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
