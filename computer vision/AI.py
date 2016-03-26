from ImageProcessing import *

def AI(ball_x,ball_y,ball_x_pre,ball_y_pre):
    #get BALL SPEED
    #ball_diff_x = ball_cur[0] - ball_pre[0]
    #ball_diff_y = ball_cur[1] - ball_pre[1]
    #ball_speed = ball_diff_y*ball_diff_y +ball_diff_x*ball_diff_x


    #things to work with : path , speed , x , y cooridnates of ball
    rod_pos_r1l= ballFollowPostion(ball_x,ball_y)
    rod_pos_r2l  = rod_pos_r1l
    rod_pos_r1r = randomRotation()
    rod_pos_r2r = randomRotation()

    print ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre)

    return(rod_pos_r1l,rod_pos_r1r,rod_pos_r2l,rod_pos_r2r)

########DEFNESE TACTICS#######3333333333333
def ballFollowPostion(ball_x,ball_y): # follow the ball
    """
    :param ball_x:
    :param ball_y:
    :return: position of first player
    """
    p = 0
    if(ball_y-FOOSMAN_WIDTH/2-0.3)>3*FOOSMAN_DISTANCE:
        p =  90
    elif(ball_y-FOOSMAN_WIDTH/2-0.3)>2*FOOSMAN_DISTANCE:
        p =  (ball_y-FOOSMAN_WIDTH/2)-2*FOOSMAN_DISTANCE
    elif(ball_y-FOOSMAN_WIDTH/2-0.3)>FOOSMAN_DISTANCE:
        p =  (ball_y-FOOSMAN_WIDTH/2)-FOOSMAN_DISTANCE
    elif(ball_y-FOOSMAN_WIDTH/2-0.3)>0:
        p =  (ball_y-FOOSMAN_WIDTH/2)
    return p


def ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre):
    intersecting = [[False,0],[False,0]]   # intercting and which path it intersects
    y = [[False,0],[False,0]]
    path = find_ball_path(ball_cur = [ball_x,ball_y] , ball_pre = [ball_x_pre,ball_y_pre])

    print path
    #print ("time for path find " + str(time_total))
    #print ("array size " + str(len(path)))
    #print ("ROW friendly   " + str(ROW_FRIENDLY[0]) + "   " +  str(ROW_FRIENDLY[1]))

    #find which rods intrecting
    for i in range(0,len(path)):
        for j in range(0,len(ROW_FRIENDLY)):
            x =0 ;

            if((ROW_FRIENDLY[j]>path[i][0][0] and ROW_FRIENDLY[j] < path[i][1][0]) or (ROW_FRIENDLY[j]<path[i][0][0] and ROW_FRIENDLY[j]>path[i][1][0]) ):
                intersecting[j][0] = True;
                intersecting[j][1] = i

                #find equation of line
                m = (path[i][1][1] - path[i][0][1]) / (path[i][1][0] - path[i][0][0])
                c = path[i][1][1] - m*path[i][1][0]

                #find y coodinate
                y[j][0] = True
                y[j][1] = m * ROW_FRIENDLY[j] + c
    return y


def randomRotation():
    return (random.randint(-90,90))

AI(250,250,240,240)