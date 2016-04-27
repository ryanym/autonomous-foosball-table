#from AI import * #Ai makes use of mudle_test so prevent recusrsive inclusion
from Rod import Rod
from ImageProcessing import *
from Communication import Communication

from AI import  ball_FollowBallPath

r1 = Rod(0)
r2 = Rod(1)
comm = Communication('COM3')

###############################
cam_open,cap = SetupCam()

while(cam_open):
    hsv_edge,frame_field = getHSV(cap)
    cv2.imshow('frame_field',frame_field)

    ##### GET BALL POS #####
    ball_x,ball_y,ball_found = getBallPosition(frame_field)   # ball position in mm.
    # print ball_x, ball_y
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
    if ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre)[0][0]:
        predY = ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre)[0][1]
    else:
        predY = ball_y
    int(predY)
    # comm.moveTo(r1.move(predY,ball_x))
    comm.moveTo(r1.move(ball_y - BALL_R/2.0, ball_x),r2.move(ball_y - BALL_R/2.0, ball_x))
    # r1.move(ball_y,ball_x)
    ball_x_pre = ball_x
    ball_y_pre = ball_y

    predY_pre = predY
    # print comm.getCurrentSteps();

    # print ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre)
    # print comm.getCurrentSteps()
    time.sleep(0.12)
# When everything done,home motors and release the capture
print 'before home'
comm.home()
print 'after home'
# r1.homeRod()

comm.closeComm()
cap.release()
cv2.destroyAllWindows()
