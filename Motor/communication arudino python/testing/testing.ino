#include "pin_def.h"
/*The data to be sent should be comma delimited ex 4,5,6,7, the last comma is importatnt as well
 * When changing the number of receivevd varaibles make sure you change on the PC side
 * Program currently configred to do stuff with 4 vairables
 * 
 */
 //constants
 #define pi 3.14
 #define counter_clockwise -1
 #define clockwise 1
 
//four motors going from row1_linear,row1_rotational,row2_linear,row2_rotational
//max size is 32767 for each integer...do not go above this limit


 //Safety is false but turns true if system needs to stop

 
//number of data to be received
int num_receive = 5;
int Read = 0 ;                            //to signify if anything has entered serial
bool Safety = false;                     //need to be true if shit happens and system needs to stop

//motor
int linear_steps = 200;                  //steps/rev for linear motors
int rotational_steps = 200;              //steps /rev for rotational motor
int motor_delay = 10;                    //in microseconds  between setting motor pin high and low
int motor_pins[4] = {0,0,0,0};           //the motors pins which are set high and low to force motor movement
int Move[4] = {0,0,0,0};                 //actual lenghts and angles to move
int motor_current[4] ={0,0,0,0};         //current step postion of motors
int steps_to_move[4] = {0,0,0,0};        //numer of steps to move
int polarity_pins[4] = {0,0,0,0};        //for clockwise or anticlockwise rotation

//linear Gear
int num_teeth = 30;                              //num of teeth on rotaional gear for linear tranlation
int spacing_teeth  = 0.2;                        //in cm since as input of length is in cm


void setup() {
  // put your setup code here, to run once:
  enable_pins();
  Serial.begin(9600);
  Serial.print("RESET");

  //so motors do not urn more than they are supposed ot. FOr rotational there are no consideraitons
  //for linear it should notgo beyond 8.5 cm
}

void loop() {
  Serial_Read(Move,&Safety);
  
  //funciton in move motor doc
  //convert_to_steps(steps_to_move,Move,motor_current);
  //move_motor(steps_to_move[0],steps_to_move[1],steps_to_move[2],steps_to_move[3]);  
  delay(10);
}







