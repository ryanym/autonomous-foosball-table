from numpy import *
from ImageProcessing import *


class Rod:

    def __init__(self, rodNumber):
        self.rodNumber = rodNumber
        self.ball_y_pre = 0
        self.ball_x_pre = 0
        self.prevP = 0
        self.kicked = False
        self.prekick = False
        self.oscillated = False
        self.lin = 0
        self.rot = 0

    def home(self):
        print 'homing rod'
        # return [0,0,0,0]
        return [100,0,0,0]
    def absPos(self, ball_y):

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

    def absPos2(self, y):

        curP = 0.0

        if (y  - FOOSMAN_WIDTH / 2.0 )< FOOSMAN_DISTANCE:
            curP=0
        else:
            curP = (y - FOOSMAN_WIDTH / 2.0) - FOOSMAN_DISTANCE
        if curP > 88.0:
            curP = 88.0
        int(round(curP))
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
    def oscillate(self, p1, p2):
        if not self.oscillated:
            self.oscillated = not self.oscillated
            return self.absPos2(p1)
        else:
            self.oscillated = not self.oscillated
            return self.absPos2(p2)


    def move(self,y,x):
        p1 = array([400, 112])
        p2 = array([400, 184])
        pball = array([x, y])
        pr0s = array([168, 0])
        pr0e = array([168, 270])
        pr1s = array([338, 0])
        pr1e = array([338, 270])

        if self.canKickForward(x):
            if self.rodNumber == 0:
                if not self.kicked :
                    self.rot = 45
                    self.kicked = True
                else:
                    self.rot = 0
                    self.kicked = False
            if self.rodNumber == 1:
                if not self.kicked:
                    self.rot = 5
                    self.kicked = True
                else:
                    self.rot = 0
                    self.kicked = False

        elif self.canKickBackward(x,y):
            if not self.kicked:
                if self.rodNumber == 0:
                    self.rot = 5
                else:
                    self.rot = -45
                self.kicked = True
            else:
                self.rot = 0
                self.kicked = False
        else:
            self.rot = 0

        if self.rodNumber == 1 and not self.canKickForward(x):
            self.lin = self.oscillate(self.intersect(p1,pball,pr1s) + BALL_R, self.intersect(p2, pball, pr1s)- BALL_R)
            # self.lin = self.oscillate(112,184)
            self.lin = int(self.lin)
        else:
            self.lin = int(self.absPos(y))
        # self.lin = int(self.ballFollowPosition(y))
        if (self.rodNumber == 0):
            pos = [self.lin,self.rot,0,0]
        else:
            pos = [0,0,self.lin,self.rot]

        return pos

    def intersect(self, p1, pball,prls):
        y_diff = p1[0]-pball[0]
        y_diff_rod = prls[0] - pball[0]
        ratio = y_diff_rod / y_diff
        return pball[1] + (p1[1] -pball[1] )*ratio

