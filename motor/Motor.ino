#include "pin_def.h"
/*The data to be sent should be comma delimited ex 4,5,6,7, the last comma is importatnt as well
 * When changing the number of receivevd varaibles make sure you change on the PC side
 */
 
 //constants
 #define pi 3.14
 #define counter_clockwise -1
 #define clockwise 1
 
/*four motors going from row1_linear,row1_rotational,row2_linear,row2_rotational
max size is 32767 for each integer...do not go above this limit*/

/* Safety is false but turns true if system needs to stop */
bool safety = false;
 
/* number of data to be received */
int Read = 0 ;                            //to signify if anything has entered serial   
long baudrate = 9600;
   
/* Serial read confirmed. So movement funcitons only run when needed to */
bool serial_read,mid_serial_read = false;       
      
/* motor properties */
int linear_steps = 200;                  //steps/rev for linear motors
int rotational_steps = 200;              //steps /rev for rotational motor
int motor_moved[4] = {false,false,false,false};

/*  delays also used for movement as well as homing */ //200 works for motor_delay
int motor_delay = 1000;                    //in microseconds  between setting motor pin high and low
int after_motor_delay = 100;
int between_motor_delay = 0;
int polarity_delay = 2000;
int homing_delay = motor_delay+1000;

/* PIN configuration */
int motor_control_pins[4] = {X_STEP_PIN  ,E_STEP_PIN  ,Y_STEP_PIN  ,Q_STEP_PIN  };           //the motors pins which are set high and low to force motor movement
int polarity_pins[4] = {X_DIR_PIN,E_DIR_PIN,Y_DIR_PIN,Q_DIR_PIN};        //for clockwise or anticlockwise rotation
int sensor_pins[4][2] = {{X_MIN_PIN,X_MAX_PIN},{0,0},{0,0},{0,0}};       //two for linear
int stop_pin  = STOP_PIN;

/* arrays actively manipualted */
float lengths_angles[4] = {0,0,0,0};                 //actual lenghts and angles to move
int motor_current[4] ={0,0,0,0};         //current step postion of motors
int steps_to_move[4] = {0,0,0,0};        //numer of steps to move
int reset_array[4][2] = {  {0,316},       //316 steps corresponds to 95mm
                            {0,0},
                            {0,0},
                            {0,0}
                            };
/* linear gear properties */
int num_teeth = 30;                              //num of teeth on rotaional gear for linear tranlation
float spacing_teeth  = 2;                        //in cm since as input of length is in mm

/* time keeping */
long time_start,time_end,time_elapsed,time1,time2,time3,time4,time5 = 0;

void setup() {
  /* enable all pins */
  enable_pins();
  delay(100);

  /* begin Serial config */
  serial_config();

  /*setup interrupt*/
  //attachInterrupt(digitalPinToInterrupt(STOP_PIN), stop_button_interupt , CHANGE);
  //pinMode(STOP_PIN , INPUT);

  /* home motors */
  //homing(motor_current);

}

void loop() {
  /* Check if serial data avaible */
  ReadSteps(lengths_angles,&safety);

  if(serial_read == true || mid_serial_read == true){
    convert_to_steps(steps_to_move,lengths_angles,motor_current);
    move_motor(steps_to_move[0],steps_to_move[1],steps_to_move[2],steps_to_move[3]);  
    serial_read = false;
  }
}












