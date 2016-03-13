import serial
import time
#serial port number should be = COM# - 1

#return a string sperated by commas for sending over serial comm
#ex [3,4,5,6,3] = "3,4,5,6,3"
#there has to be a comma at the end to signify ending of characters
def array_to_string(x):
    str_send = ""
    for j in range(0,len(x)):
            str_send = str_send + str(x[j])+","
    return(str_send)
    
#825,500,1000,0.3 for linear
#1000,950,1000,0.3 for rotaioanal
motor_delay = 820;
after_delay = 500;
polarity_delay = 1000;
time_sleep = 0.4;
#p2 = [200,1100,200,200,'t']
#n2 = [-200,1100,200,200,'t']
l1 = [8,0,0,0,'t',motor_delay,after_delay,polarity_delay]
l2 = [0,0,0,0,'t',motor_delay,after_delay,polarity_delay]
r1 = [1,360,0,0,'t',motor_delay,after_delay,polarity_delay]
r2 = [4,0,4,0,'t',motor_delay,after_delay,polarity_delay]

home = [0,0,0,0,'t',motor_delay,after_delay,polarity_delay]

#only works with 5 valuess as the Arduino is expecting 4 integers and one chara
#@parma = [int row1_linear,int row1_roational,int row2_linear,int row2_roational,character t or f)
#ex [1,2,3,4,t]
def R2(x):
    #array to be sent
    #x=[3,4,5,6]
    #turning on serial
    #serARD = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600);
    COM_Port = 18;
    serARD = serial.Serial((COM_Port-1), 9600);
    #printing the serial port conencted to
    print serARD.name

    data =0;
    i=0;
    j=0;

    #converting arrray into a sendable string
    str_send = array_to_string(x)

    #writing the string to the serial port
    serARD.write(str_send);
    
    #readinf data and printing it
    #data = serARD.read(2);
    #data = serARD.read(len(str(data_write))+1);
    print data

    #important to close
    serARD.close()
    
for i in range(10):
    R2(l1)
    time.sleep(time_sleep)
    R2(l2)
    time.sleep(time_sleep)


#R2(r1);
#print( "R2");
#time.sleep(time_sleep)
#R2(l2);
#time.sleep(time_sleep)
R2(home);
            

    

#notes on implementation
#send a byte to start the signal
#wait for inf returned ---> must know how many bytes are sent back
#TESTS
#see how many bytes neede for expect4ed values of characters
#PROBELMS
#arduino resets on serial comm which can be resolved by using a capactor between RESET and 5V

#end - goal = send 4 numbers and a confirmation bit of either 0 or 1
