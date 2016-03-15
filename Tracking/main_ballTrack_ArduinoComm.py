from module_test_v0 import *

###############################
cam_open,cap = SetupCam()
while(cam_open):
    hsv_edge,frame_field = getHSV(cap)
    cv2.imshow('frame_field',frame_field)
    ball_x,ball_y,ball_found = getBallPosition(frame_field)   # ball position in mm.
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
    rod_position = getPosition(ball_x,ball_y)/10
    print ball_x,ball_y, rod_position
    

    #################ARDUINO INTERFACE ##################
    time.sleep(0.25);
    test = [rod_position, 0, 0, 0, 't', motor_delay, after_delay, polarity_delay]
    #R2(test);
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
