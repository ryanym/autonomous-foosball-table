#Image Processing
def ImageProcessing(camera_frame):
    dst = cv2.filter2D(camera_frame,-1,kernel)
    hsv_frame = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    return hsv_frame

#Ball Detection
def BallDetection(hsv_frame):
    lowerb = np.array([LOWER_H,LOWER_S,LOWER_V])
    upperb = np.array([UPPER_H,UPPER_S,UPPER_V])
    dest_image = cv2.inRange(hsv_frame, lowerb, upperb)
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER_DIL,1)
    cv2.imshow("Ball",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    findBall = False
    radiusMax = 4
    m_ball_x = -1
    m_ball_y = -1
    ballCenter = (-1,-1)
    if len(contours) >0:
        for cnt in contours:
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            if radius >4 and radius <10:
                findBall = True
                if radius > radiusMax:
                    radiusMax = radius
                    ballCenter = center
                    m_ball_x = int(x)
                    m_ball_y = int(y)
        if findBall == False:
            print 'Ball not shown'
        else:
            print ballCenter
            cv2.circle(frame,ballCenter,radiusMax,(0,255,0),2)      
    else:
        print 'undetected'

    m_ball_found = findBall
    return (m_ball_x,m_ball_y,m_ball_found)
    


#Foosman Detection 
def FoosmanDetection(hsv_frame):
    first_fil_img = cv2.inRange(hsv_frame, ROB_LOWHSV, ROB_UPPHSV)
    dilate = cv2.dilate(first_fil_img,REC_ERROR_FILTER_DIL,1)
    cv2.imshow("Robot Image",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    detectRec(contours,frame)

    #unfinished
    if len(contours) >0:
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            if(w<10 or h<16 ): continue
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            recCenter=(int(x+w/2),int(y+h/2))
            #cv2.circle(fram,recCenter,(255,0,0),3,3)
            print recCenter
    else:
        print 'undetected'
