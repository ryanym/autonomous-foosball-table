import serial
import time

#motor props
MOTOR_STEPS = 200
SPACING_TEETH = 2
NUM_TEETH = 30


'''
    return a string sperated by commas with an endline character 'n' for sending over serial comm
    ex [3,4,5,6,3] = "3,4,5,6,3,n"
    there has to be a comma at the end to signify ending of characters
'''
def array_to_string(x):
    str_send = ""
    for j in range(0, len(x)):
        str_send = str_send + str(x[j]) + ","
    str_send += "n"
    return (str_send)

'''
    @parma = [float row1_linear,float row1_roational,float row2_linear,float row2_roational,character t or f)
'''
def moveTo(x):
    COM_Port = 8;
    # turning on serial
    # serARD = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600);
    serARD = serial.Serial(port='COM18',baudrate=9600)
    # printing the serial port conencted to
    # print serARD.name
    # print (x)

    # converting arrray into a sendable string
    str_send = array_to_string(x)
    # print("move rod to: %s" % str_send)
    # writing the string to the serial port
    serARD.write(str_send);

    # readinf data and printing it

    time_start = time.clock()


    # important to close
    serARD.close()

'''
    return : array of motor absolute positions [l1,r1,l2,r2]
'''
def getCurrentSteps():
    returnList = [0,0,0,0]
    time_start = time.clock()

    serARD.write("0n")    #just send one random charcacter
    data = serARD.readline()
    mylist = [int(x) for x in data.split(',')]
    time_end = time.clock() - time_start;

    returnList[0] = steps2Linear(mylist[0])
    returnList[1] = steps2Rotaional(mylist[1])
    returnList[2] = steps2Linear(mylist[2])
    returnList[3] = steps2Rotaional(mylist[3])
    return(returnList)

TIME_SLEEP = 0.15;
# p2 = [200,1100,200,200,'t']
l1 = [80, 360, 80, 360]
l2 = [0, 0, 0, 0]
r1 = [10, 360, 0, 0]
r2 = [40, 0, 4, 0]

home = [0, 0, 0, 0]

def test():
    for i in range(15):
        moveTo(l1)
        time.sleep(TIME_SLEEP)
        moveTo(home)
        time.sleep(TIME_SLEEP)
    moveTo(home)

def steps2Linear(steps):
     length_per_steps = (float(SPACING_TEETH) * NUM_TEETH) / MOTOR_STEPS
     return(length_per_steps * steps)

def steps2Rotaional(steps):
    return(steps*360.0/MOTOR_STEPS)



# #testing out how fast i can recevie serial
# moveTo(home)
# time.sleep(1)
#
# moveTo(l1);
# serARD = serial.Serial(port='COM11',baudrate=9600)

# serARD.close()


''' NOTE
  -arduino resets on serial comm which can be resolved by using a capactor between RESET and 5V
'''


