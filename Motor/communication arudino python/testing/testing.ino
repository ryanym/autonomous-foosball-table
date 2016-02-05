/*The data to be sent should be comma delimited ex 4,5,6,7, the last comma is importatnt as well
 * When changing the number of receivevd varaibles make sure you change on the PC side
 * Program currently configred to do stuff with 4 vairables
 */
 
//four motors going from row1_linear,row1_rotational,row2_linear,row2_rotational
//max size is 32767 for each integer...do not go above this limit
 int Move[4] = {0,0,0,0};

 //Safety is false but turns true if system needs to stop
 bool Safety = false;
 
 //number of data to be received
 //code must be changed as right now onyl the motor buffers are being filled
int num_receive = 5;

 //to signify if anything has entered serial
int Read = 0 ;

//linear Gear
int num_teeth = 30;
int spacing_teeth  = 0.360; 

//motor
int steps_rev = 200;
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.print("RESET");
}

void loop() {
  Serial_Read(Move,&Safety);
  Move_Motor();
}





