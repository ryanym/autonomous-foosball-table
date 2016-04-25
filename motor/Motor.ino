// BOF preprocessor bug prevent - insert me on top of your arduino-code
#if 1
__asm volatile ("nop");
#endif

/************** INCLUDES ***********************************************/
#include "pin_def.h"
#include <avr/io.h> 
#include <avr/wdt.h>
 
/********************* DEFINES ***************************/
#define pi 3.14
#define counter_clockwise -1
#define clockwise 1
#define SERIAL_PRINT    //for Serial print taht are not necessary


/************************ VARIABLES ************************************/
/* Safety is false but turns true if system needs to stop */
bool safety = false;
 
/* Serial props */
long baudrate = 57600;
   
/* Serial read confirmed. So movement funcitons only run when needed to */
bool serial_read_flag,mid_serial_read_flag = false;       
      
/* motor properties */
int linear_steps = 200;                  //steps/rev for linear motors
int rotational_steps = 200;              //steps /rev for rotational motor

/*  delays also used for movement as well as homing */ //200 works for motor_delay
int motor_delay = 1000;                    //in microseconds  between setting motor pin high and low
int after_motor_delay = 300;
int between_motor_delay = 0;
int polarity_delay = 2000;
int homing_delay = motor_delay+1000;
int serial_motor_delay = 500;

/* PIN configuration */
int motor_control_pins[4] = {X_STEP_PIN  ,E_STEP_PIN  ,Y_STEP_PIN  ,Q_STEP_PIN  };           //the motors pins which are set high and low to force motor movement
int polarity_pins[4] = {X_DIR_PIN,E_DIR_PIN,Y_DIR_PIN,Q_DIR_PIN};        //for clockwise or anticlockwise rotation
int sensor_pins[4][2] = {{X_MIN_PIN,X_MAX_PIN},{0,0},{0,0},{0,0}};       //two for linear
int stop_pin  = STOP_PIN;

/* arrays actively manipualted */
float lengths_angles[4] = {0,0,0,0};                 //actual lenghts and angles to move
int motor_current[4] ={0,0,0,0};         //current step postion of motors
int steps_to_move[4] = {0,0,0,0};        //numer of steps to move
int reset_array[4][2] = {  {16,293},       //316 steps corresponds to 95mm.this is for when the swithces are hit
                            {0,0},
                            {0,0},
                            {0,0} };
int motor_moved[4] = {false,false,false,false};    //flag to indicate individual motor step

/* linear gear properties */
int num_teeth = 30;                              //num of teeth on rotaional gear for linear tranlation
float spacing_teeth  = 2;                        //in cm since as input of length is in mm

/* time keeping */
long time_start,time_end,time_elapsed,time1,time2,time3,time4,time5 = 0;

/************************************* SETUP ***************************/
void setup() {
  /* enable all pins */
  enable_pins();
  delay(100);

  /* begin Serial config */
  serial_config();

  /* clear reset pin */
  clear_reset_bit();
  
  /*setup interrupt*/
  //attachInterrupt(digitalPinToInterrupt(STOP_PIN), stop_button_interupt , CHANGE);
  //pinMode(STOP_PIN , INPUT);

  /* home motors */
  homing();

}

/************************ LOOP ************************************s******/

void loop() {
  /* Check if serial data avaible */
  ReadSteps();

  if(serial_read_flag == true || mid_serial_read_flag == true){
    convert_to_steps();
    move_motor();  
    serial_read_flag = false;
  }
}












