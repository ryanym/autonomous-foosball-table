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
            curP = 88.0
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
        elif self.rodNumber == 1:
            if x >= 300 and x <= 330:
                return True
    def canKickBackward(self, x, y):
        if self.rodNumber == 0:
            if x >= 180 and x <= 200:
                return True
        # kicking towards wall but not goal
        elif self.rodNumber == 1:
            if x >= 330 and (y <= 110 or y >= 190):
                return True
    # def osilate(self, p1, p2):


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
        elif self.canKickBackward(x,y):
            if not self.kicked:
                if self.rodNumber == 0:
                    rot = 5
                else:
                    rot = 45
                self.kicked = True
            else:
                rot = 0
                self.kicked = False
        else:
            rot = 0

        lin = int(self.ballFollowPosition(y))
        # lin = self.ballFollowPosition(y)
        if (self.rodNumber == 0):
            pos = [lin,rot,0,0]
        else:
            pos = [0,0,lin,rot]

        return pos
        # print self.canKickForward(x), self.prekick, self.kicked
        # print pos
        # moveTo(pos)