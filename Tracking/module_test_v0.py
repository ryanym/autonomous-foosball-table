'''
by Chenhe, Roland
November 14, 2015
ball tracking and path prediction
ball path prediction only does on reflection on the long side
'''
import numpy as np
import cv2
import time
from arduino import *


#constants
CAM_ID = 1
CAM_WIDTH = 320
CAM_HEIGHT = 240
CAM_FPS = 120

'''
The Edge of the playfield, use for cut capture image
new coordinte after cut
0,0                         0,EDGE_Y_MAX-EDGE_Y_MIN-1
EDGE_X_MAX-EDGE_X_MIN-1,0     EDGE_X_MAX-EDGE_X_MIN-1,EDGE_Y_MAX-EDGE_Y_MIN-1
'''

EDGE_X_MIN = 20
EDGE_X_MAX = 302
EDGE_Y_MIN = 18
EDGE_Y_MAX = 220

FIELD_L = 410 # mm
FIELD_W = 290 # mm
FIELD_L_PIXEL = EDGE_X_MAX - EDGE_X_MIN
FIELD_W_PIXEL = EDGE_Y_MAX - EDGE_Y_MIN
ROW_1 = 55 #mm
ROW_2 = 155 #mm
ROW_3 = 255 #mm
ROW_4 = 357 #mm

ROW_TOL = 10 #mm
ROW_1_PIXEL = FIELD_L_PIXEL*ROW_1/FIELD_L
ROW_2_PIXEL = FIELD_L_PIXEL*ROW_2/FIELD_L
ROW_3_PIXEL = FIELD_L_PIXEL*ROW_3/FIELD_L
ROW_4_PIXEL = FIELD_L_PIXEL*ROW_4/FIELD_L
ROW_TOL_PIXEL = FIELD_L_PIXEL*ROW_TOL/FIELD_L

FOOSMAN_DISTANCE = 88 #mm
FOOSMAN_WIDTH =24 #mm
FOOSMAN_DISTANCE_PIXEL = FIELD_L_PIXEL*FOOSMAN_DISTANCE/FIELD_L
FOOSMAN_WIDTH_PIXEL = FIELD_L_PIXEL*FOOSMAN_WIDTH/FIELD_L
#BALL radiues in pixel
BALL_R = 14 #mm
BALL_R_MIN = 4 #pixel
BALL_R_MAX = 12 #pixel
BALL_R_PIXEL = int(BALL_R * FIELD_L_PIXEL / FIELD_L )
#Ball center moving area
BALL_X_MAX = FIELD_L - BALL_R -1
BALL_Y_MAX = FIELD_W - BALL_R - 1
BALL_X_MIN = BALL_R
BALL_Y_MIN = BALL_R

GOAL_W = 90#mm
GOAL_L = 23#mm
GOAL_W_PIXEL = FIELD_W_PIXEL*GOAL_W/FIELD_W
GOAL_L_PIXEL = FIELD_L_PIXEL*GOAL_L/FIELD_L
# xmin,xmax,ymin,ymax (pixel)
GOAL_USER = [0,GOAL_L_PIXEL,     (FIELD_W_PIXEL-GOAL_W_PIXEL)/2,(FIELD_W_PIXEL+GOAL_W_PIXEL)/2]
GOAL_ROB = [FIELD_L_PIXEL-GOAL_L_PIXEL-1,FIELD_L_PIXEL-1,  (FIELD_W_PIXEL-GOAL_W_PIXEL)/2,(FIELD_W_PIXEL+GOAL_W_PIXEL)/2]

BALL_SPEED_Square_MIN = 3

L_PTOMM =  1.0*FIELD_L / FIELD_L_PIXEL
W_PTOMM =  1.0*FIELD_W / (FIELD_W_PIXEL)

print L_PTOMM
print W_PTOMM

#BALL color
hsv = None
LOWER_H = 96
LOWER_S = 112
LOWER_V = 128
UPPER_H = 116
UPPER_S = 180
UPPER_V = 239

GOAL_LOWHSV = np.array([92,116,62])
GOAL_UPPHSV = np.array([112,183,99])

ROB_LOWHSV = np.array([0,60,159])
ROB_UPPHSV = np.array([11,235,255])

USER_LOWHSV = np.array([0,0,230])
USER_UPPHSV = np.array([179,36,255])

EDGE_LOWHSV = np.array([60,0,0])
EDGE_UPPHSV = np.array([115,255,255])

	
ERROR_FILTER = np.ones((2,2),np.uint8)

def nothing(x):
    pass

def find_ball_path(ball_cur,ball_pre):
    path = []
    ball_tar = [None] * 2
    ball_diff_x = ball_cur[0] - ball_pre[0]
    ball_diff_y = ball_cur[1] - ball_pre[1]
    ball_speed = ball_diff_y*ball_diff_y +ball_diff_x*ball_diff_x
    if ball_speed < BALL_SPEED_Square_MIN:
        return path;
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
            ball_tar[1]  = ball_cur[1] + (ball_tar[0] - ball_cur[0])/ball_diff_x*ball_diff_y
            
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
            ball_tar[1]  = ball_cur[1] + (ball_tar[0] - ball_cur[0])/ball_diff_x*ball_diff_y
            
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

def w_ptomm(pixels):
    return pixels*W_PTOMM;

def l_ptomm(pixels):
    return pixels*L_PTOMM;


def foosmen_location(foosmen):
    #input array of (x,y_center,w,h)
    foosmen_relocate = -1;
    if len(foosmen) >= 3:
        foosmen.sort(key=lambda tup: tup[2]*tup[3], reverse = True)
        foosmen = foosmen[0:3]
        foosmen.sort(key=lambda tup: tup[1])
        tmp_middle = (foosmen[0][1]+foosmen[2][1])/2
        foosmen_middle = ();
        foosmen_middle = min(foosmen, key=lambda foosman:abs(foosman[1]-tmp_middle))
        foosmen_relocate = w_ptomm(foosmen_middle[1])
    return foosmen_relocate


################################################################################################################################ 
def getRowPosition(hsv):
    first_fil_img = cv2.inRange(hsv, ROB_LOWHSV, ROB_UPPHSV)
    erosion = cv2.erode(first_fil_img,ERROR_FILTER,1)
    dilate = cv2.dilate(erosion,ERROR_FILTER,1)
    cv2.imshow("robot foosmen",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(contours, key = cv2.contourArea, reverse = True)

    row2 = [];
    row4 = [];
    for cnt in c:
            x,y,w,h = cv2.boundingRect(cnt)
            if (h < 30)and(w>4)and (h>4):
                if x+w+ROW_TOL_PIXEL > ROW_2_PIXEL and x-ROW_TOL_PIXEL < ROW_2_PIXEL:
                    row2.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,255,0),2)
                if x+w+ROW_TOL_PIXEL > ROW_4_PIXEL and x-ROW_TOL_PIXEL < ROW_4_PIXEL:
                    row4.append((x,y+h/2,w,h))
    foosmen_location(row2);
    foosmen_location(row4);

    row2_linear = foosmen_location(row2);
    row4_linear = foosmen_location(row4);
    return row2_linear,row4_linear

def getEnemyPosition(hsv):
    first_fil_img = cv2.inRange(hsv, USER_LOWHSV, USER_UPPHSV)
    erosion = cv2.erode(first_fil_img,ERROR_FILTER,1)
    dilate = cv2.dilate(erosion,ERROR_FILTER,1)
    cv2.imshow("user foosmen",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(contours, key = cv2.contourArea, reverse = True)

    row1 = [];
    row3 = [];
    for cnt in c:
            x,y,w,h = cv2.boundingRect(cnt)
            if (h < 30)and(w>4)and (h>5):
                if x+w+ROW_TOL_PIXEL > ROW_1_PIXEL and x-ROW_TOL_PIXEL < ROW_1_PIXEL:
                    row1.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,0,255),2)
                if x+w+ROW_TOL_PIXEL > ROW_3_PIXEL and x-ROW_TOL_PIXEL < ROW_3_PIXEL:
                    row3.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,0,255),2)
    row1_linear = foosmen_location(row1);
    row3_linear = foosmen_location(row3);
    return row1_linear,row3_linear


'''
#set up campture
cap = cv2.VideoCapture(CAM_ID)
cap.set(3,CAM_WIDTH)
cap.set(4,CAM_HEIGHT)
cap.set(5,CAM_FPS)
'''
#Filter
lowerb = np.array([LOWER_H,LOWER_S,LOWER_V])
upperb = np.array([UPPER_H,UPPER_S,UPPER_V])
kernel = np.ones((5,5),np.float32)/25

kernel_edge = np.ones((3,3),np.float32)/9
kernel_foosmen = np.ones((3,3),np.float32)/9
ball_pre = (-1,-1)
ball_cur = (-1,-1)
###############################
def SetupCam():
    CAM_ID = 1
    CAM_WIDTH = 320
    CAM_HEIGHT = 240
    CAM_FPS = 90
    cap = cv2.VideoCapture(CAM_ID)
    if(cap.isOpened()):
        cap.set(3,CAM_WIDTH)
        cap.set(4,CAM_HEIGHT)
        cap.set(5,CAM_FPS)
        return (True,cap)
    else:
        return (False,cap)

def getHSV(cap):
    ret, frame = cap.read()
    cv2.imshow('foolcapture',frame)
    dst = cv2.filter2D(frame,-1,kernel)
    #frame_field = frame[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    '''
    hsv_edge = [None,None,None,None]
    hsv_edge[0] = hsv[0:EDGE_Y_MIN,0:CAM_WIDTH]
    hsv_edge[1] = hsv[EDGE_Y_MAX:CAM_HEIGHT,0:CAM_WIDTH]
    hsv_edge[2] = hsv[0:CAM_HEIGHT,0:EDGE_X_MIN]
    hsv_edge[3] = hsv[0:CAM_HEIGHT,EDGE_X_MAX:CAM_WIDTH]
    '''
    hsv_edge = (hsv[0:EDGE_Y_MIN,0:CAM_WIDTH],hsv[EDGE_Y_MAX:CAM_HEIGHT,0:CAM_WIDTH],hsv[0:CAM_HEIGHT,0:EDGE_X_MIN],hsv[0:CAM_HEIGHT,EDGE_X_MAX:CAM_WIDTH])
    frame_field = hsv[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]
    return hsv_edge,frame_field

def getBallPosition(hsv):  # return true position in mm
    dest_image = cv2.inRange(hsv, lowerb, upperb)
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER,1)
    cv2.imshow("Ball",dilate)
    a,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    ball_found = False
    ball_cur = (-1,-1)
    ball_radius_max = 4
    ball_center = (-1,-1)
    if len(contours) >0:
        for cnt in contours:
            (x,y),tmp_radius = cv2.minEnclosingCircle(cnt)
            if tmp_radius >BALL_R_MIN and tmp_radius <BALL_R_MAX:
                ball_found = True
                if tmp_radius > ball_radius_max:
                    ball_cur = (x,y)  
    return ((ball_cur[0]*L_PTOMM,ball_cur[1]*W_PTOMM),ball_found)

def getUnknown(hsv_edge):
     #0,1 compare with x-axis; 2,3 compare with y-axis
    #return true when unknown detected, else false
    for edge_index in [0,1]:
            edge_fil_img = cv2.inRange(hsv_edge[edge_index], EDGE_LOWHSV, EDGE_UPPHSV) 
            dilate = cv2.dilate(edge_fil_img,ERROR_FILTER,1)
            asfdas,contours,hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            c = sorted(contours, key = cv2.contourArea, reverse = True)
            edge_cover = {'x':0,'w':0}#y,h
            for cnt in c:
                x,y,w,h = cv2.boundingRect(cnt)
                '''
                if(w>edge_cover['w']):
                    edge_cover['w'] = w
                    edge_cover['x'] = x
                '''
                if  x < EDGE_X_MIN and x+w > EDGE_X_MAX:
                    edge_cover['w'] = w
                    edge_cover['x'] = x
                    break
            #print edge_cover
            cv2.imshow("edge"+str(edge_index),edge_fil_img) 
            if  edge_cover['x']> EDGE_X_MIN or edge_cover['x']+edge_cover['w']< EDGE_X_MAX:
                return True
            
                
    for edge_index in [2,3]:
            edge_fil_img = cv2.inRange(hsv_edge[edge_index], EDGE_LOWHSV, EDGE_UPPHSV)
            dilate = cv2.dilate(edge_fil_img,ERROR_FILTER,1)
            asfdas,contours,hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            c = sorted(contours, key = cv2.contourArea, reverse = True)
            edge_cover = {'y':0,'h':0}#y,h
            for cnt in c:
                x,y,w,h = cv2.boundingRect(cnt)
                '''
                if(h>edge_cover['h']):
                    edge_cover['h'] = h
                    edge_cover['y'] = y
                '''
                if  y < EDGE_Y_MIN and y+h > EDGE_Y_MAX:
                    edge_cover['h'] = h
                    edge_cover['y'] = y
                    break
            #print edge_cover
            cv2.imshow("edge"+str(edge_index),edge_fil_img)
            if  edge_cover['y']> EDGE_Y_MIN or edge_cover['y']+edge_cover['h']< EDGE_Y_MAX:
                return True
    return False


def getGoal(hsv):
    ball_radius_max = 4
    goalR = False
    goalU=False
    goal_user_area = hsv[GOAL_USER[2]:GOAL_USER[3],GOAL_USER[0]:GOAL_USER[1]]
    goal_rob_area = hsv[GOAL_ROB[2]:GOAL_ROB[3],GOAL_ROB[0]:GOAL_ROB[1]]
    #detect user goal 
    dest_image = cv2.inRange(goal_user_area, GOAL_LOWHSV,GOAL_UPPHSV)
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER,1)
    cv2.imshow('goal_rob_area',dilate)
    a,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    user_ball_radius_max = 4
    ball_center = (-1,-1)
    if len(contours) >0:
        for cnt in contours:
            (x,y),tmp_radius = cv2.minEnclosingCircle(cnt)
            if tmp_radius >BALL_R_MIN and tmp_radius <BALL_R_MAX:
                if tmp_radius > ball_radius_max:
                    user_ball_radius_max = tmp_radius
    #detect rob goal 
    dest_image = cv2.inRange(goal_rob_area, GOAL_LOWHSV,GOAL_UPPHSV)
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER,1)
    cv2.imshow('goal_user_area',dilate)
    a,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    rob_ball_radius_max = 4
    ball_center = (-1,-1)
    if len(contours) >0:
        for cnt in contours:
            (x,y),tmp_radius = cv2.minEnclosingCircle(cnt)
            if tmp_radius >BALL_R_MIN and tmp_radius <BALL_R_MAX:
                if tmp_radius > ball_radius_max:
                    rob_ball_radius_max = tmp_radius
                    ball_cur = (x,y)
    #if  rob_ball_radius_max==user_ball_radius_max or (rob_ball_radius_max ==4 and user_ball_radius_max == 4): 
    #    return goalR_goalU
    if rob_ball_radius_max> user_ball_radius_max: 
        goalR=True
    if rob_ball_radius_max< user_ball_radius_max: 
        goalU=True
    return (goalR,goalU)


def getPosition(ball_x,ball_y): # follow the ball
    p = 0
    if(ball_y-FOOSMAN_WIDTH/2-0.3)>3*FOOSMAN_DISTANCE:
        p =  88
    elif(ball_y-FOOSMAN_WIDTH/2-0.3)>2*FOOSMAN_DISTANCE:
        p =  (ball_y-FOOSMAN_WIDTH/2)-2*FOOSMAN_DISTANCE
    elif(ball_y-FOOSMAN_WIDTH/2-0.3)>FOOSMAN_DISTANCE:
        p =  (ball_y-FOOSMAN_WIDTH/2)-FOOSMAN_DISTANCE
    elif(ball_y-FOOSMAN_WIDTH/2-0.3)>0:
        p =  (ball_y-FOOSMAN_WIDTH/2)
    return p



ball_cur = (250,250)
ball_pre = (240,240)
path = find_ball_path(ball_cur,ball_pre)
print path



###############################

'''
cam_open,cap = SetupCam()
while(cam_open):
    hsv_edge,frame_field = getHSV(cap)
    cv2.imshow('frame_field',frame_field)
    ball_cur,ball_found = getBallPosition(frame_field)   # ball position in mm.
    path = find_ball_path(ball_cur,ball_pre)
    ball_pre =ball_cur;


    #getRowPosition(frame_field);
    #getEnemyPosition(frame_field);
    #unkown = getUnknown(hsv_edge)
    if(ball_found == False):
        Rob,User = getGoal(frame_field)
        print Rob,User
    #else:
        #print ball_x,ball_y
    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
    ################ AI ###################################
    rod_position = getPosition(ball_cur[0],ball_cur[1])/10
    print ball_cur[0],ball_cur[1], rod_position
    
    print getRowPosition(frame_field)
    #print getEnemyPosition(frame_field)
    #################ARDUINO INTERFACE ##################
    #time.sleep(0.25);
    #test = [rod_position, 0, 0, 0, 't', motor_delay, after_delay, polarity_delay]
    #R2(test);
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



'''
