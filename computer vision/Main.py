from AI import * #Ai makes use of mudle_test so prevent recusrsive inclusion
from Rod import Rod

r1 = Rod(0)
###############################
cam_open,cap = SetupCam()

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
    ################ AI ###################################
    # rod_pos_r1l , rod_pos_r1r , rod_pos_rod_posi_r2l , rod_pos_r2r = AI(ball_x,ball_y,ball_x_pre,ball_y_pre)
    # print ball_x,ball_y, rod_pos_r1l

    #################ARDUINO INTERFACE ##################
    time.sleep(0.2)
    # test = [rod_pos_r1l, rod_pos_r1r, rod_pos_r1l, rod_pos_r2r]
    # testp = r1.ballFollowPosition(ball_x,ball_y)
    # test = [testp,0, 0, 0]
    #
    #
    # if(testp):
    #     moveTo(test)
    # print ball_x
    r1.move(ball_y,ball_x)


# When everything done,home motors and release the capture
print 'before home'
r1.homeRod()
print home
print 'after home'
# r1.homeRod()
cap.release()
cv2.destroyAllWindows()
