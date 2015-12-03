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
CAM_ID = 1
CAM_WIDTH = 320
CAM_HEIGHT = 240
CAM_FPS = 90

'''
The Edge of the playfield, use for cut capture image
new coordinte after cut
0,0                         0,EDGE_Y_MAX-EDGE_Y_MIN-1
EDGE_X_MAX-EDGE_X_MIN-1,0     EDGE_X_MAX-EDGE_X_MIN-1,EDGE_Y_MAX-EDGE_Y_MIN-1
'''

EDGE_X_MIN = 20
EDGE_X_MAX = 304
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
FOOSMAN_WIDTH =28 #mm
FOOSMAN_DISTANCE_PIXEL = FIELD_L_PIXEL*FOOSMAN_DISTANCE/FIELD_L
FOOSMAN_WIDTH_PIXEL = FIELD_L_PIXEL*FOOSMAN_WIDTH/FIELD_L
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

GOAL_W = 90#mm
GOAL_L = 23#mm
GOAL_W_PIXEL = FIELD_W_PIXEL*GOAL_W/FIELD_W
GOAL_L_PIXEL = FIELD_L_PIXEL*GOAL_L/FIELD_L
# xmin,xmax,ymin,ymax
GOAL_USER = [0,GOAL_L_PIXEL,     (FIELD_W_PIXEL-GOAL_W_PIXEL)/2,(FIELD_W_PIXEL+GOAL_W_PIXEL)/2]
GOAL_ROB = [FIELD_L_PIXEL-GOAL_L_PIXEL-1,FIELD_L_PIXEL-1,  (FIELD_W_PIXEL-GOAL_W_PIXEL)/2,(FIELD_W_PIXEL+GOAL_W_PIXEL)/2]

BALL_SPEED_Square_MIN = 3
print 1.0*FIELD_L_PIXEL / FIELD_L
print 1.0*FIELD_W_PIXEL / FIELD_W


#BALL color
hsv = None
LOWER_H = 92
LOWER_S = 112
LOWER_V = 148
UPPER_H = 116
UPPER_S = 183
UPPER_V = 239


GOAL_LOWHSV = np.array([92,116,62])
GOAL_UPPHSV = np.array([112,183,99])
ROB_LOWHSV = np.array([0,60,159])
ROB_UPPHSV = np.array([24,235,255])
USER_LOWHSV = np.array([0,0,235])
USER_UPPHSV = np.array([179,36,255])
EDGE_LOWHSV = np.array([60,0,0])
EDGE_UPPHSV = np.array([115,255,255])

	
ERROR_FILTER = np.ones((2,2),np.uint8)
ERROR_FILTER_MEN = np.ones((2,2),np.uint8)
ERROR_FILTER_EDGE = np.ones((4,4),np.uint8)
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



def foosmen_location(foosmen):
    #input array of (x,y_center,w,h)
    foosmen_relocate = []
    if len(foosmen) >= 3:
        foosmen.sort(key=lambda tup: tup[2]*tup[3], reverse = True)
        foosmen = foosmen[0:3]
        foosmen.sort(key=lambda tup: tup[1])
        tmp_middle = (foosmen[0][1]+foosmen[2][1])/2
        foosmen_middle = ();
        foosmen_middle = min(foosmen, key=lambda foosman:abs(foosman[1]-tmp_middle))
        for i in (-1,0,1):
            foosmen_relocate.append( (foosmen_middle[0],
                                      foosmen_middle[0]+foosmen_middle[2],
                                      foosmen_middle[1]-FOOSMAN_WIDTH_PIXEL/2+i*FOOSMAN_DISTANCE_PIXEL,
                                      foosmen_middle[1]+FOOSMAN_WIDTH_PIXEL/2+i*FOOSMAN_DISTANCE_PIXEL) )
    '''
    if len(foosmen)==2:
        foosmen.sort(key=lambda tup: tup[2])
        foosmen_middle = ()
        tmp_middle = (foosmen[0][2]+foosmen[1][2])/2
        if tmp_middle < FIELD_W_PIXEL/2:
            foosmen_middle = foosmen[1]
        if tmp_middle >= FIELD_W_PIXEL/2:
            foosmen_middle = foosmen[0]
        for i in (-1,0,1):
            foosmen_relocate.append( (foosmen_middle[0],
                                      foosmen_middle[1],
                                      foosmen_middle[2]-FOOSMAN_WIDTH_PIXEL/2+i*FOOSMAN_DISTANCE_PIXEL,
                                      foosmen_middle[2]+FOOSMAN_WIDTH_PIXEL/2+i*FOOSMAN_DISTANCE_PIXEL) )
    '''
    return foosmen_relocate
    

def unknown_detect(hsv):
    #0,1 compare with x-axis; 2,3 compare with y-axis
    #return true when unknown detected, else false
    hsv_edge = (hsv[0:EDGE_Y_MIN,0:CAM_WIDTH],hsv[EDGE_Y_MAX:CAM_HEIGHT,0:CAM_WIDTH],hsv[0:CAM_HEIGHT,0:EDGE_X_MIN],hsv[0:CAM_HEIGHT,EDGE_X_MAX:CAM_WIDTH])
    for edge_index in [0,1]:
            edge_fil_img = cv2.inRange(hsv_edge[edge_index], EDGE_LOWHSV, EDGE_UPPHSV) 
            dilate = cv2.dilate(edge_fil_img,ERROR_FILTER_EDGE,1)
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
            dilate = cv2.dilate(edge_fil_img,ERROR_FILTER_EDGE,1)
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
                print edge_cover
                return True
    return False

#set up campture
cap = cv2.VideoCapture(CAM_ID)
cap.set(3,CAM_WIDTH)
cap.set(4,CAM_HEIGHT)
cap.set(5,CAM_FPS)
#Filter
lowerb = np.array([LOWER_H,LOWER_S,LOWER_V])
upperb = np.array([UPPER_H,UPPER_S,UPPER_V])
kernel = np.ones((7,7),np.float32)/49

kernel_edge = np.ones((3,3),np.float32)/9

ball_pre = (-1,-1)
ball_cur = (-1,-1)

while(True):

    ret, frame = cap.read()
    dst = cv2.filter2D(frame,-1,kernel)
    frame_field = frame[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    '''
    hsv_edge = [None,None,None,None]
    hsv_edge[0] = hsv[0:EDGE_Y_MIN,0:CAM_WIDTH]
    hsv_edge[1] = hsv[EDGE_Y_MAX:CAM_HEIGHT,0:CAM_WIDTH]
    hsv_edge[2] = hsv[0:CAM_HEIGHT,0:EDGE_X_MIN]
    hsv_edge[3] = hsv[0:CAM_HEIGHT,EDGE_X_MAX:CAM_WIDTH]
    '''
    unkown = unknown_detect(hsv)
    if(unkown):
        print 'unkown detected'        
    
    hsv = hsv[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]

    cv2.line(frame_field,(BALL_X_MIN,BALL_Y_MIN),(BALL_X_MAX,BALL_Y_MIN),(0,255,0),2,8,0)
    cv2.line(frame_field,(BALL_X_MIN,BALL_Y_MAX),(BALL_X_MAX,BALL_Y_MAX),(0,255,0),2,8,0)
    cv2.line(frame_field,(ROW_1_PIXEL,0),(ROW_1_PIXEL,FIELD_W_PIXEL),(0,0,255),2,8,0)
    cv2.line(frame_field,(ROW_2_PIXEL,0),(ROW_2_PIXEL,FIELD_W_PIXEL),(0,255,0),2,8,0)
    cv2.line(frame_field,(ROW_3_PIXEL,0),(ROW_3_PIXEL,FIELD_W_PIXEL),(0,0,255),2,8,0)
    cv2.line(frame_field,(ROW_4_PIXEL,0),(ROW_4_PIXEL,FIELD_W_PIXEL),(0,255,0),2,8,0)
    
    

    dest_image = cv2.inRange(hsv, lowerb, upperb)
    #reduce noise
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER,1)
    cv2.imshow("Ball",dilate)
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
        if ball_found == False :
            #print 'Ball not found'
            ball_pre = (-1,-1)
            ball_cur = (-1,-1)
        else:
            if ball_pre[0] >0 and ball_cur[0] >0:
                print 'preBall ',center_ftoi(ball_pre),'currentBall ',center_ftoi(ball_cur)
                ball_path = find_ball_path(ball_cur,ball_pre)
                #print ball_path
                for line in ball_path:
                    cv2.line(frame_field,center_ftoi(line[0]),center_ftoi(line[1]),(255,0,0),2,8,0)
                #cv2.line(frame,center_ftoi(ball_cur),center_ftoi((ball_cur[0]+(ball_cur[0]-ball_pre[0])*40,ball_cur[1]+(ball_cur[1]-ball_pre[1])*40)),(0,255,0),2,8,0)
            ball_pre = ball_cur
            cv2.circle(frame_field,center_ftoi(ball_cur),int(tmp_radius),(255,0,0),2)
    if(ball_found == False):
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
        if  rob_ball_radius_max==user_ball_radius_max or (rob_ball_radius_max ==4 and user_ball_radius_max == 4): 
            print 'ball undetected'
        if rob_ball_radius_max> user_ball_radius_max: 
            print 'rob goal'
        if rob_ball_radius_max< user_ball_radius_max: 
            print 'user goal'
    


    first_fil_img = cv2.inRange(hsv, USER_LOWHSV, USER_UPPHSV)
    erosion = cv2.erode(first_fil_img,ERROR_FILTER_MEN,1)
    dilate = cv2.dilate(first_fil_img,ERROR_FILTER_EDGE,1)
    cv2.imshow("Rectangle Image",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(contours, key = cv2.contourArea, reverse = True)
    row1=[]
    row2=[]
    row3=[]
    row4=[]
    for cnt in c:
            x,y,w,h = cv2.boundingRect(cnt)
            if (h < 30)and(w>4)and (h>4):    
                if x+w+ROW_TOL_PIXEL > ROW_2_PIXEL and x-ROW_TOL_PIXEL < ROW_2_PIXEL:
                    row2.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,255,0),2)
                if x+w+ROW_TOL_PIXEL > ROW_4_PIXEL and x-ROW_TOL_PIXEL < ROW_4_PIXEL:
                    row4.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,255,0),2)
    first_fil_img = cv2.inRange(hsv, ROB_LOWHSV, ROB_UPPHSV)
    erosion = cv2.erode(first_fil_img,ERROR_FILTER_MEN,1)
    dilate = cv2.dilate(first_fil_img,ERROR_FILTER_MEN,1)
    cv2.imshow("Rectangle Image1",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(contours, key = cv2.contourArea, reverse = True)
    for cnt in c:
            x,y,w,h = cv2.boundingRect(cnt)
            if (h < 30)and(w>4)and (h>5):
                if x+w+ROW_TOL_PIXEL > ROW_1_PIXEL and x-ROW_TOL_PIXEL < ROW_1_PIXEL:
                    row1.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,0,255),2)
                if x+w+ROW_TOL_PIXEL > ROW_3_PIXEL and x-ROW_TOL_PIXEL < ROW_3_PIXEL:
                    row3.append((x,y+h/2,w,h))
                    #cv2.rectangle(frame_field,(x,y),(x+w,y+h),(0,0,255),2)

    row1_foosmen = foosmen_location(row1)
    for i in row1_foosmen:
        cv2.rectangle(frame_field,(i[0],i[2]),(i[1],i[3]),(0,0,255),2)
    
    row3_foosmen = foosmen_location(row3)
    for i in row3_foosmen:
        cv2.rectangle(frame_field,(i[0],i[2]),(i[1],i[3]),(0,0,255),2)
    row2_foosmen = foosmen_location(row2)
    for i in row2_foosmen:
        cv2.rectangle(frame_field,(i[0],i[2]),(i[1],i[3]),(0,255,0),2)
    row4_foosmen = foosmen_location(row4)
    for i in row4_foosmen:
        cv2.rectangle(frame_field,(i[0],i[2]),(i[1],i[3]),(0,255,0),2)
            
    #cv2.imshow('frame',frame)
    cv2.imshow('field',frame_field)
    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
