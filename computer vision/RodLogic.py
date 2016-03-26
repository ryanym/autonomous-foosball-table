from Communication import *
from ImageProcessing import *

class Rod:

    def __init__(self, rodNumber):
        self.rodNumber = rodNumber

    def homeRod(self):
        print 'homing rod'
        moveTo(home)

    def ballFollowPostion(ball_x, ball_y):
        p = 0
        if (ball_y - FOOSMAN_WIDTH / 2 - 0.3) > 3 * FOOSMAN_DISTANCE:
            p = 90
        elif (ball_y - FOOSMAN_WIDTH / 2 - 0.3) > 2 * FOOSMAN_DISTANCE:
            p = (ball_y - FOOSMAN_WIDTH / 2) - 2 * FOOSMAN_DISTANCE
        elif (ball_y - FOOSMAN_WIDTH / 2 - 0.3) > FOOSMAN_DISTANCE:
            p = (ball_y - FOOSMAN_WIDTH / 2) - FOOSMAN_DISTANCE
        elif (ball_y - FOOSMAN_WIDTH / 2 - 0.3) > 0:
            p = (ball_y - FOOSMAN_WIDTH / 2)
        return p



