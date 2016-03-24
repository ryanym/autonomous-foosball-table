from module_test_v0 import *

def AI(ball_x,ball_y,ball_x_pre,ball_y_pre):
    #get BALL SPEED
    #ball_diff_x = ball_cur[0] - ball_pre[0]
    #ball_diff_y = ball_cur[1] - ball_pre[1]
    #ball_speed = ball_diff_y*ball_diff_y +ball_diff_x*ball_diff_x

    # get BALL PATH
    #path = find_ball_path(ball_cur = [ball_x,ball_y] ,ball_pre = [ball_x_pre,ball_y_pre])

    #things to work with : path , speed , x , y cooridnates of ball
    rod_pos_r1l= ballFollowPostion(ball_x,ball_y)
    rod_pos_r2l  = rod_pos_r1l
    rod_pos_r1r = randomRotation()
    rod_pos_r2r = randomRotation()
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


def ball_FollowBallPath(ball_x,ball_y):
    x=0;

def randomRotation():
    return (random.randint(-90,90))