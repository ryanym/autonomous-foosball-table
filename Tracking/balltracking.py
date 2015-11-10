import numpy as np
import cv2
import time

def nothing(x):
    pass

camID = 1
camWidth =320
camHeight = 240

hsv = None
LOWER_H = 92
LOWER_S = 112
LOWER_V = 162
UPPER_H = 116
UPPER_S = 183
UPPER_V = 236

ERROR_FILTER = np.ones((3,3),np.uint8)
ERROR_FILTER_DIL = np.ones((4,4),np.uint8)

def detectRec(cont,fram):
    if len(cont) >0:
        for cnt in cont:
            x,y,w,h = cv2.boundingRect(cnt)
            center = (int(x),int(y))
            cv2.rectangle(fram,(x,y),(x+w,y+h),(0,255,0),2)
            recCenter=(int((x+w)/2),int((y+h)/2))
            print recCenter
    else:
        print 'undetected'

def setWindowTrackBars():
    #cv2.namedWindow("Image",flags=cv2.WINDOW_NORMAL)
    cv2.namedWindow("Trackbar", flags=cv2.WINDOW_NORMAL)
    #cv2.namedWindow("Binary Image",flags=cv2.WINDOW_NORMAL)
    cv2.createTrackbar("LowerH","Trackbar",0,180,on_changeLH)
    cv2.createTrackbar("UpperH","Trackbar",0,180,on_changeUH)
    cv2.createTrackbar("LowerS","Trackbar",0,255,on_changeLS)
    cv2.createTrackbar("UpperS","Trackbar",0,255,on_changeUS)
    cv2.createTrackbar("LowerV","Trackbar",0,255,on_changeLV)
    cv2.createTrackbar("UpperV","Trackbar",0,255,on_changeUV)
    
def getThresholdImg():
    global hsv
    if hsv.any():
        #print hsv
        lowerb = np.array([LOWER_H,LOWER_S,LOWER_V])
        upperb = np.array([UPPER_H,UPPER_S,UPPER_V])
       # print lowerb
       # print upperb
        dest_image = cv2.inRange(hsv, lowerb, upperb)
        cv2.imshow("Binary Image",dest_image)
        return dest_image
    
def on_changeLH(value):
    global LOWER_H
    LOWER_H = value
    getThresholdImg()

def on_changeUH(value):
    global UPPER_H
    UPPER_H = value
    getThresholdImg()

def on_changeLS(value):
    global LOWER_S
    LOWER_S = value
    getThresholdImg()

def on_changeUS(value):
    global UPPER_S
    UPPER_S = value
    getThresholdImg()

def on_changeLV(value):
    global LOWER_V
    LOWER_V = value
    getThresholdImg()

def on_changeUV(value):
    global UPPER_V
    UPPER_V = value
    getThresholdImg()
    
def mouseListener(event, x, y, flags, img):
    global hsv
    if event==cv2.EVENT_LBUTTONDOWN:
        print "The HSV values at this point are: "
        print hsv[y, x]


cap = cv2.VideoCapture(camID)
cap.set(3,camWidth)
cap.set(4,camHeight)
#cap.set(5,120)
setWindowTrackBars()
lowerb = np.array([LOWER_H,LOWER_S,LOWER_V])
upperb = np.array([UPPER_H,UPPER_S,UPPER_V])
kernel = np.ones((3,3),np.float32)/9

rec_lowerb = np.array([0,99,192])
rec_upperb = np.array([21,194,255])
while(True):
    ret, frame = cap.read()
    dst = cv2.filter2D(frame,-1,kernel)
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    dest_image = cv2.inRange(hsv, lowerb, upperb)
    #cv2.imshow("Binary Image",dest_image)
    
    erosion = cv2.erode(dest_image,ERROR_FILTER,1)
    dilate = cv2.dilate(dest_image,ERROR_FILTER_DIL,1)
    
    cv2.imshow("Binary Image",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    findBall = False
    radiusMax = 4;
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
        if findBall == False:
            print 'Ball not shown'
        else:
            print ballCenter
            cv2.circle(frame,ballCenter,radiusMax,(0,255,0),2)
    else:
        print 'undetected'
        
    #Detect Rectangle
    hsv_new = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    first_fil_img = cv2.inRange(hsv, rec_lowerb, rec_upperb)
    erosion = cv2.erode(first_fil_img,ERROR_FILTER,1)
    dilate = cv2.dilate(first_fil_img,ERROR_FILTER_DIL,1)
    cv2.imshow("Rectangle Image",dilate)
    asfdas,contours,hierarchy = cv2.findContours(dilate, 1, 2)
    detectRec(contours,frame)
    
    #Rectangle End
    
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()




'''
img = cv2.imread("a.jpg")
kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(img,-1,kernel)

hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
#h: 0-180, .*2; s and v: 0-255, .%255
getThresholdImg()
setWindowTrackBars()
cv2.imshow("Image", dst)
cv2.setMouseCallback("Image", mouseListener, dst)
c=cv2.waitKey(0)
#Press "ESC" to exit
if c==27:
     cv2.destroyAllWindows()
'''    





"""
maxCamTested = 10
camWidth = 320
camHeight = 240
camID = 0
def countCameras():
    i = 0
    while(i<maxCamTested):
        cap = cv2.VideoCapture(i)
        time.sleep(0.5)
        res = cap.isOpened()
        time.sleep(0.5)
        cap.release()
        if (res ==0):
            return i
        i=i+1
    return maxCamTested

print time.time()
time.sleep(0.05)
print time.time()


numCam = countCameras()
print numCam


#set up campture
cap = cv2.VideoCapture(camID)
cap.set(3,camWidth)
cap.set(4,camHeight)
cap.set(5,100)

while(True):
    t = cv2.getTickFrequency();
    print t
    try:
        print cap.get(cv2.CAP_PROP_FPS)
    except:
        print 'sd'

    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    t = (cv2.getTickCount() - t) / cv2.getTickFrequency()
    print t,"I am working at ",1000000/t," FPS"
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
"""


