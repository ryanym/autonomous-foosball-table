#from AI import * #Ai makes use of mudle_test so prevent recusrsive inclusion
from Rod import Rod
from ImageProcessing import *
from Communication import Communication
import random
from AI import  ball_FollowBallPath

r1 = Rod(0)
r2 = Rod(1)
comm = Communication('COM3')
comm.home()

###############################
cam_open,cap = SetupCam()
counter = 0
randint = random.randint(50, 200)

while(cam_open):
    hsv_edge,frame_field = getHSV(cap)
    cv2.imshow('frame_field',frame_field)

    ##### GET BALL POS #####
    ball_x,ball_y,ball_found = getBallPosition(frame_field)   # ball position in mm.
    if(ball_found == False):
        Rob,User = getGoal(frame_field)
        print Rob,User

    ##### PRESS q FOR EXIT########
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

    ####### CALCULATE OPTIMAL POSITIONS and SEND TO CONTROLLER #####################

    if(counter<randint):
        counter =  counter + 1;
        comm.moveTo(r1.move(ball_y, ball_x), r2.move(ball_y, ball_x), getUnknown(hsv_edge))
        #####DELAY#######
        time.sleep(0.08)

    else:
        comm.home()
        counter = 0;
        randint = random.randint(50, 200)
        time.sleep(0.17)



# When everything done,home motors and release the capture
print 'before home'
comm.home()
print 'after home'
# r1.homeRod()

comm.closeComm()
cap.release()
cv2.destroyAllWindows()
