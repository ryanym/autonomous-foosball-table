from Communication import *
from ImageProcessing import *


class Rod:

    def __init__(self, rodNumber):
        self.rodNumber = rodNumber
        self.ball_y_pre = 0
        self.ball_x_pre = 0
        self.prevP = 0
        self.kicked = False
        self.prekick = False

    def home(self):
        print 'homing rod'
        # return [0,0,0,0]
        return [100,0,0,0]
    def ballFollowPosition(self,ball_y):

        curP = 0
        if (ball_y - FOOSMAN_WIDTH / 2.0 - 0.3) > 3 * FOOSMAN_DISTANCE:
            curP = 95
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
            if x >= 125 and x <= 160:
                return True
    def move(self,y,x):
        global lin, rot
        if self.canKickForward(x):
            if not self.kicked and not self.prekick:
                rot = -45
                self.prekick = True
            elif not self.kicked and self.prekick:
                rot = 45
                self.kicked  = True
            else:
                rot = 0
                self.kicked = False
                self.prekick = False
        else:
            rot = 0

        lin = int(self.ballFollowPosition(y))
        # lin = self.ballFollowPosition(y)
        pos = [lin,rot,0,0]
        print "predict:", pos

        return pos
        # print self.canKickForward(x), self.prekick, self.kicked
        # print pos
        # moveTo(pos)