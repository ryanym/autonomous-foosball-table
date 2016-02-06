import serial

def rotate(steps):
	serARD = serial.Serial(port='/dev/cu.usbmodem1421', baudrate=9600)
	
	print serARD.name
	data = 0
    #send data
	print "printing sent data:"
	serARD.write(str(steps))
	print str(steps)

    #readinf data and printing it
	print "printing recieved data:"
	data = serARD.readline()
	print str(data)

    #important to close
	serARD.close()

rotate(200)