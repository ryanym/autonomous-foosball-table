#include "pin_def.h"
/*The data to be sent should be comma delimited ex 4,5,6,7, the last comma is importatnt as well
 * When changing the number of receivevd varaibles make sure you change on the PC side
 * Program currently configred to do stuff with 4 vairables
 */
 //constants
 #define pi 3.14
 #define counter_clockwise -1
 #define clockwise 1
 
//four motors going from row1_linear,row1_rotational,row2_linear,row2_rotational
//max size is 32767 for each integer...do not go above this limit
 int Move[4] = {0,0,0,0};
 int motor_current[4] ={0,0,0,0};
 int steps_to_move[4] = {0,0,0,0};

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
int linear_steps = 200;
int rotational_steps = 200;
int motor_delay = 10;    //in microseconds
int motor_pins[4] = {0,0,0,0};

//pin for setting to clokwise when high
int polarity_pins[4] = {0,0,0,0};



void setup() {
  // put your setup code here, to run once:
  enable_pins();
  Serial.begin(9600);
  Serial.print("RESET");
}

void loop() {
  Serial_Read(Move,&Safety);
  
  //funciton in move motor doc
  //convert_to_steps(steps_to_move,Move,motor_current);
  //move_motor(steps_to_move[0],steps_to_move[1],steps_to_move[2],steps_to_move[3]);
  

  
  delay(10);
}





