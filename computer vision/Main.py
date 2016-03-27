#from AI import * #Ai makes use of mudle_test so prevent recusrsive inclusion
from Rod import Rod
from ImageProcessing import *
from Communication import *

r1 = Rod(0)
###############################
cam_open,cap = SetupCam()
serARD = serial.Serial(port='COM3', baudrate=9600)

while(cam_open):
    hsv_edge,frame_field = getHSV(cap)
    cv2.imshow('frame_field',frame_field)

    ##### GET BALL POS #####
    ball_x,ball_y,ball_found = getBallPosition(frame_field)   # ball position in mm.

    #getRowPosition(frame_field);
    #getEnemyPosition(frame_field);
    #unkown = getUnknown(hsv_edge)
    if(ball_found == False):
        Rob,User = getGoal(frame_field)
        print Rob,User
    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break



    # test = [rod_pos_r1l, rod_pos_r1r, rod_pos_r1l, rod_pos_r2r]
    # testp = r1.ballFollowPosition(ball_x,ball_y)
    # test = [testp,0, 0, 0]
    #
    #
    # if(testp):
    #     moveTo(test)
    # print ball_x
    r1.move(ball_y,ball_x)
    time.sleep(0.2)


# When everything done,home motors and release the capture
print 'before home'
r1.homeRod()
print home
print 'after home'
# r1.homeRod()
serARD.close()
cap.release()
cv2.destroyAllWindows()
