from Communication import *
from ImageProcessing import *

class Rod:



    def __init__(self, rodNumber):
        self.rodNumber = rodNumber
        self.ball_y_pre = 0
        self.ball_x_pre = 0
        self.prevP = 0
        self.kicked = False
    def homeRod(self):
        print 'homing rod'
        moveTo(home)

    def ballFollowPosition(self,ball_y):

        curP = 0
        if (ball_y - FOOSMAN_WIDTH / 2.0 - 0.3) > 3 * FOOSMAN_DISTANCE:
            curP = 90.0
        elif (ball_y - FOOSMAN_WIDTH / 2.0 - 0.3) > 2 * FOOSMAN_DISTANCE:
            curP = (ball_y - FOOSMAN_WIDTH / 2.0) - 2 * FOOSMAN_DISTANCE
        elif (ball_y - FOOSMAN_WIDTH / 2.0 - 0.3) > FOOSMAN_DISTANCE:
            curP = (ball_y - FOOSMAN_WIDTH / 2.0) - FOOSMAN_DISTANCE
        elif (ball_y - FOOSMAN_WIDTH / 2.0 - 0.3) > 0:
            curP = (ball_y - FOOSMAN_WIDTH / 2.0)

        int(round(curP))
        # curP = int(round(curP))
        if abs(self.prevP - curP) > 5:
            # print (abs(self.ball_y_prey_pre - curP))
            self.prevP = curP
            return curP
        else:
            return self.prevP

    def canKickForward(self, x):
        if self.rodNumber == 0:
            if x >= 120 and x <= 160:
                return True
    def move(self,y,x):
        if self.canKickForward(x) and not self.kicked:
            rot = 60
            self.kicked = True
        else:
            rot = 0
            self.kicked = False
        lin = self.ballFollowPosition(y)
        pos = [lin,rot,0,0]
        print self.canKickForward(x), self.kicked
        print pos
        moveTo(pos)