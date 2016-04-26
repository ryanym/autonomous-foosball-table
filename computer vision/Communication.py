import serial
import time

#motor props
MOTOR_STEPS = 200
SPACING_TEETH = 2
NUM_TEETH = 30

# p2 = [200,1100,200,200,'t']
#testing purposes
l1 = [80, 360, 80, 360]
l2 = [0, 0, 0, 0]
r1 = [10, 360, 0, 0]
r2 = [40, 0, 4, 0]
home = [0, 0, 0, 0]
TIME_SLEEP = 0.15;

class Communication():

    def __init__(self,COM_NUM):
        self.serARD = serial.Serial(port=COM_NUM, baudrate=9600)

    def array_to_string(self, x):
        '''return a string sperated by commas with an endline character 'n' for sending over serial comm
        ex [3,4,5,6,3] = "3,4,5,6,3,n"
        there has to be a comma at the end to signify ending of characters
        '''
        str_send = ""
        for j in range(0, len(x)):
            str_send = str_send + str(x[j]) + ","
        str_send += "n"
        return str_send



    def moveTo(self, pos_ang0, pos_ang1):
        '''para : array[float row1_linear,float row1_roational,float row2_linear,float row2_roational,character t or f)
        '''
        # serARD = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600);
        combined_pos = [x + y for x, y in zip(pos_ang0, pos_ang1)]
        print combined_pos
        str_send = self.array_to_string(combined_pos)
        self.serARD.write(str_send)

    def home(self):
        home = [0,0,0,0,'h']
        str_send = self.array_to_string(home)
        self.serARD.write(str_send)



    def steps2Linear(self,steps):
        '''converts steps to absolute linear'''
        length_per_steps = (float(SPACING_TEETH) * NUM_TEETH) / MOTOR_STEPS
        return length_per_steps * steps

    def steps2Rotaional(self,steps):
        '''converts ot absolute angle'''
        return steps*360.0/MOTOR_STEPS

    def getCurrentSteps(self):
        '''get current absolute postions from controller - takes 17ms ish
        send only one random character with character 'n'
        '''
        returnlist = [0, 0, 0, 0]
        self.serARD.write("0n")
        data = self.serARD.readline()
        mylist = [int(x) for x in data.split(',')]

        returnlist[0] = self.steps2Linear(mylist[0])
        returnlist[1] = self.steps2Rotaional(mylist[1])
        returnlist[2] = self.steps2Linear(mylist[2])
        returnlist[3] = self.steps2Rotaional(mylist[3])
        return returnlist

    def closeComm(self):
        self.serARD.close()





'''
    return a string sperated by commas with an endline character 'n' for sending over serial comm
    ex [3,4,5,6,3] = "3,4,5,6,3,n"
    there has to be a comma at the end to signify ending of characters
'''
# def array_to_string(x):
#     str_send = ""
#     for j in range(0, len(x)):
#         str_send = str_send + str(x[j]) + ","
#     str_send += "n"
#     return (str_send)
#
# '''
#     @parma = [float row1_linear,float row1_roational,float row2_linear,float row2_roational,character t or f)
# '''
# def moveTo(x):
#
#     # serARD = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600);
#     serARD = serial.Serial(port='COM3',baudrate=9600)
#     str_send = array_to_string(x)
#     serARD.write(str_send);
#     # important to close
#     serARD.close()
#
# '''
#     return : array of motor absolute positions [l1,r1,l2,r2]
# '''
# def getCurrentSteps():
#     returnList = [0, 0, 0, 0]
#     time_start = time.clock()
#
#     serARD.write("0n")    #just send one random charcacter
#     data = serARD.readline()
#     mylist = [int(x) for x in data.split(',')]
#     time_end = time.clock() - time_start;
#
#     returnList[0] = steps2Linear(mylist[0])
#     returnList[1] = steps2Rotaional(mylist[1])
#     returnList[2] = steps2Linear(mylist[2])
#     returnList[3] = steps2Rotaional(mylist[3])
#     return(returnList)
#
#
# def test():
#     for i in range(15):
#         moveTo(l1)
#         time.sleep(TIME_SLEEP)
#         moveTo(home)
#         time.sleep(TIME_SLEEP)
#     moveTo(home)
#
# def steps2Linear(steps):
#      length_per_steps = (float(SPACING_TEETH) * NUM_TEETH) / MOTOR_STEPS
#      return length_per_steps * steps
#
# def steps2Rotaional(steps):
#     return steps*360.0/MOTOR_STEPS
#
#
#
# # #testing out how fast i can recevie serial
# # moveTo(home)
# # time.sleep(1)
# # #
# # moveTo(l1);
# # time.sleep(1)
# # serARD = serial.Serial(port='COM18',baudrate=9600)
# # print getCurrentSteps()
# # serARD.close()
#
#
# ''' NOTE
#   -arduino resets on serial comm which can be resolved by using a capactor between RESET and 5V
# '''
#
#
