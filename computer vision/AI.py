from ImageProcessing import *
ROW_FRIENDLY = [ROW_2,ROW_4]
#### FLAGS
defense_flag = False;
offense_flag = False;
kick_flag = False;


####rod index
l1=0;r1=1;l2=2;r2=3;
rod_pos = [0,0,0,0]

def AI(ball_x,ball_y,ball_x_pre,ball_y_pre):
    time_start2 = time.clock()
    safety_flag = 'f'
    assignDefaultPos()
    #get BALL SPEED
    #ball_diff_x = ball_cur[0] - ball_pre[0]
    #ball_diff_y = ball_cur[1] - ball_pre[1]
    #ball_speed = ball_diff_y*ball_diff_y +ball_diff_x*ball_diff_x


    #things to work with : path , speed , x , y cooridnates of ball
    # rl1,rr1,rl2,rr2
    rod_pos[l1] = ballFollowPostion(ball_y)
    rod_pos[r1] = rod_pos[l1]
    rod_pos[l2] = randomRotation()
    rod_pos[r2] = randomRotation()

    ############# ball predicted path follow ################333
    intersect =  ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre)
    if(intersect[0][0] == True):
        rod_pos[l1] = ballFollowPostion(intersect[0][1])    # ball follow converts distance to individual players
    if(intersect[1][0] == True):
        rod_pos[l2] = ballFollowPostion(intersect[1][1])

    ########## kick event ######################
    # if in front and alligned
    if(ball_x > ROW_2 and ball_x<ROW_2_MAX):
        x= 0;
    if(ball_x > ROW_4 and ball_x<ROW_4_MAX):
        x=0;
    ########## rod stuck even detect ##################

    ########### safety flag if any issues detected ####################


    return(rod_pos[l1],rod_pos[r1],rod_pos[l2],rod_pos[r2],safety_flag)

########DEFNESE TACTICS#######3333333333333
def ballFollowPostion(ball_y): # follow the ball
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

'''
return : [ [bool 1, y intersect],[bool 2,y intersect]]
'''
def ball_FollowBallPath(ball_x,ball_y,ball_x_pre,ball_y_pre):
    intersecting = [[False,0],[False,0]]   # intercting and which path it intersects
    y = [[False,0],[False,0]]
    path = find_ball_path(ball_cur = [ball_x,ball_y] , ball_pre = [ball_x_pre,ball_y_pre])

    # print path
    #print ("time for path find " + str(time_total))
    #print ("array size " + str(len(path)))
    #print ("ROW friendly   " + str(ROW_FRIENDLY[0]) + "   " +  str(ROW_FRIENDLY[1]))

    #find which rods intrecting
    for i in range(0,len(path)):
        for j in range(0,len(ROW_FRIENDLY)):
            x =0 ;

            #find if row point in between
            if((ROW_FRIENDLY[j]>path[i][0][0] and ROW_FRIENDLY[j] < path[i][1][0]) or (ROW_FRIENDLY[j]<path[i][0][0] and ROW_FRIENDLY[j]>path[i][1][0]) ):
                intersecting[j][0] = True
                intersecting[j][1] = i

                #find equation of line
                m = (path[i][1][1] - path[i][0][1]) / (path[i][1][0] - path[i][0][0])
                c = path[i][1][1] - m*path[i][1][0]

                #find y coodinate
                y[j][0] = True
                y[j][1] = m * ROW_FRIENDLY[j] + c
    return y

#random rotatoon between 90 and -90
def randomRotation():
    return(random.randint(-90,90))

def assignDefaultPos():
    rod_pos[l1] = FOOSMAN_DISTANCE / 2.0
    rod_pos[l2] = FOOSMAN_DISTANCE / 2.0
    rod_pos[r1] = 0
    rod_pos[r2] = 0

AI(250,250,240,240)
