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
    

def R(data_write):
    
    #serARD = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600);
    serARD = serial.Serial(17, 9600);
    #printing the serial port conencted to
    print serARD.name

    data =0;
    i=0;
    
    #send data
    serARD.write(str(data_write));
    
    #readinf data and printing it
    #data = serARD.read(len(str(data_write))+1);
    #print data

    #important to close
    serARD.close()

#p2 = [200,1100,200,200,'t']
#n2 = [-200,1100,200,200,'t']
#p1 = [100,1100,200,200,'t']
n1 = [2,10,2,2,'t']

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
    data = serARD.read(2);
    #data = serARD.read(len(str(data_write))+1);
    print data

    #important to close
    serARD.close()

#for i in range(10):

    #R2(n1)
    #time.sleep(1)
    #R2(p1)
    #time.sleep(1)



            

    

#notes on implementation
#send a byte to start the signal
#wait for inf returned ---> must know how many bytes are sent back
#TESTS
#see how many bytes neede for expect4ed values of characters
#PROBELMS
#arduino resets on serial comm which can be resolved by using a capactor between RESET and 5V

#end - goal = send 4 numbers and a confirmation bit of either 0 or 1
