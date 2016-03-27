from AI import * #Ai makes use of mudle_test so prevent recusrsive inclusion
from RodLogic import Rod

r1 = Rod(1)
###############################
cam_open,cap = SetupCam()
ball_x_pre=0
ball_y_pre = 0
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
    rod_pos_r1l , rod_pos_r1r , rod_pos_rod_posi_r2l , rod_pos_r2r ,safety_flag = AI(ball_x,ball_y,ball_x_pre,ball_y_pre)
    print ball_x,ball_y, rod_pos_r1l

    #################ARDUINO INTERFACE ##################

    # test = [rod_pos_r1l, rod_pos_r1r, rod_pos_r1l, rod_pos_r2r]
    test = [rod_pos_r1l,0, 0, 0]
    moveTo(test);

    time.sleep(0.2);
    ball_x_pre = ball_x
    ball_y_pre = ball_y

# When everything done,home motors and release the capture
moveTo(home)
# r1.homeRod()
cap.release()
cv2.destroyAllWindows()
