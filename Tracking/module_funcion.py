
########################################################
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



def getRowPosition(hsv):
    row1=[]
    row3=[]
    first_fil_img = cv2.inRange(hsv, ROB_LOWHSV, ROB_UPPHSV)
    erosion = cv2.erode(first_fil_img,ERROR_FILTER_MEN,1)
    dilate = cv2.dilate(first_fil_img,ERROR_FILTER_EDGE,1)
    cv2.imshow("rob foosmen",dilate)
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
     #NOT FINISHED, unclear middle position in foosmen_location

########################################

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
    frame_field = frame[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    '''
    hsv_edge = [None,None,None,None]
    hsv_edge[0] = hsv[0:EDGE_Y_MIN,0:CAM_WIDTH]
    hsv_edge[1] = hsv[EDGE_Y_MAX:CAM_HEIGHT,0:CAM_WIDTH]
    hsv_edge[2] = hsv[0:CAM_HEIGHT,0:EDGE_X_MIN]
    hsv_edge[3] = hsv[0:CAM_HEIGHT,EDGE_X_MAX:CAM_WIDTH]
    '''
    hsv_edge = hsv[EDGE_Y_MIN:EDGE_Y_MAX,EDGE_X_MIN:EDGE_X_MAX]
    return hsv_edge,frame_field


def getBallPosition(hsv):
    dest_image = cv2.inRange(hsv, lowerb, upperb)
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER,1)
    cv2.imshow("Ball",dilate)
    a,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    ball_found = False
    ball_pre = (-1,-1)
    ball_cur = (-1,-1)
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
            
            return (-1,-1,False)
        else:
            if ball_pre[0] >0 and ball_cur[0] >0:
                print 'preBall ',center_ftoi(ball_pre),'currentBall ',center_ftoi(ball_cur)
                ball_path = find_ball_path(ball_cur,ball_pre)
                #print ball_path
                #for line in ball_path:
                    #cv2.line(frame_field,center_ftoi(line[0]),center_ftoi(line[1]),(255,0,0),2,8,0)
                #cv2.line(frame,center_ftoi(ball_cur),center_ftoi((ball_cur[0]+(ball_cur[0]-ball_pre[0])*40,ball_cur[1]+(ball_cur[1]-ball_pre[1])*40)),(0,255,0),2,8,0)
            ball_pre = ball_cur
            #cv2.circle(frame_field,center_ftoi(ball_cur),int(ball_radius_max),(255,0,0),2)

    return (ball_cur[0],ball_cur[1],ball_found)


def getUnknown(hsv):
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
                return True
    return False


def getGoal(hsv):
    ball_radius_max = 4
    goalR_goalU=(False,False)
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
        return goalR_goalU
    if rob_ball_radius_max> user_ball_radius_max: 
        goalR_goalU=[True,False]
        return goalR_goalU
    if rob_ball_radius_max< user_ball_radius_max: 
        goalR_goalU=[False,True]
        return goalR_goalU
        
    
    
    
    
    


    
