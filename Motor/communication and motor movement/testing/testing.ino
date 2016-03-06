
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
bool Safety = false;
 
//number of data to be received
int num_receive = 8;
int Read = 0 ;                            //to signify if anything has entered serial
//bool Safety = false;                     //need to be true if shit happens and system needs to stop

//motor
int linear_steps = 200;                  //steps/rev for linear motors
int rotational_steps = 200;              //steps /rev for rotational motor

//moor delays also used for homing
int motor_delay = 1000;                    //in microseconds  between setting motor pin high and low
int after_motor_delay = 100;
int polarity_delay = 1500;

int motor_pins[4] = {X_STEP_PIN  ,Z_STEP_PIN  ,Y_STEP_PIN  ,E_STEP_PIN  };           //the motors pins which are set high and low to force motor movement
int Move[4] = {0,0,0,0};                 //actual lenghts and angles to move
int motor_current[4] ={0,0,0,0};         //current step postion of motors
int steps_to_move[4] = {0,0,0,0};        //numer of steps to move
int polarity_pins[4] = {X_DIR_PIN,Z_DIR_PIN,Y_DIR_PIN,E_DIR_PIN};        //for clockwise or anticlockwise rotation

//linear Gear
int num_teeth = 30;                              //num of teeth on rotaional gear for linear tranlation
float spacing_teeth  = 0.2;                        //in cm since as input of length is in cm

//motor
//int steps_rev = 200;
int counter = 0;

//Serial read confirmed. So movement funcitons only run when needed to
bool serial_read = false; 

//sensor pins 
int sensor_pins[4] = {X_MIN_PIN,0,X_MAX_PIN,0};

void setup() {
  // put your setup code here, to run once:
  enable_pins();
  delay(100);
  
  Serial.begin(9600);
  Serial.print("RESET");
  homing(motor_current);
  //so motors do not urn more than they are supposed ot. FOr rotational there are no consideraitons
  //for linear it should notgo beyond 8.5 cm. This limit should be set in the PC stage as motor controller will not be aware of it

}




void loop() {
  if(digitalRead(X_MIN_PIN)){
    digitalWrite(LED_PIN,HIGH);
  }else{
    digitalWrite(LED_PIN,LOW);
  }
  Serial.println("analogRead");
  Serial.print(digitalRead(X_MIN_PIN));
  Serial.print("  ");
  Serial.print(digitalRead(X_MAX_PIN));
 

  
  delayMicroseconds(1);
  
  Serial_Read(Move,&Safety);
 
   //step(X_STEP_PIN,Move[0],800);
  // step(Z_STEP_PIN,Move[1],800);
  
  //funciton in move motor doc
  if(serial_read == true ){
    
    convert_to_steps(steps_to_move,Move,motor_current);
    move_motor(steps_to_move[0],steps_to_move[1],steps_to_move[2],steps_to_move[3]);  
    serial_read = false;
  }
  
/*  int  steps = Move[0];
  
  if(steps < 1){  
    digitalWrite(X_DIR_PIN, LOW);
    digitalWrite(Z_DIR_PIN, LOW);
    steps = -steps;
  }
  else{
    digitalWrite(X_DIR_PIN, HIGH);
    digitalWrite(Z_DIR_PIN, HIGH);
  }

  
  if(counter < steps){
    digitalWrite(X_STEP_PIN, HIGH);
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(1000);
    digitalWrite(X_STEP_PIN, LOW);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(1000);
    counter++;    
  }
*/
}

int step(int motor, int steps, int deltaT){
  if(motor == X_STEP_PIN ){
    if(steps < 1){  
      digitalWrite(X_DIR_PIN, LOW);
      steps = -steps;
    }
    else{
      digitalWrite(X_DIR_PIN, HIGH);
    }
  }
  if(counter < steps){
    digitalWrite(motor, HIGH);
    delayMicroseconds(deltaT);
    digitalWrite(motor, LOW);
    delayMicroseconds(deltaT);
    counter++;    
  }
  return 1;
}









