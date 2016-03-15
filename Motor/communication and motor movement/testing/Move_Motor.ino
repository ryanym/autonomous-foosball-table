//r1_l = rotation linear
//assumption : motor rotates Clockwise when pin set high
//assumption : clokwise is for postive number of steps and counter is for negative
/*
 * move_motor()
 * determine_polarity();
 * move_steps()
 * get_max_val()
 * convert_to_steps()
 */
void move_motor(int r1_l,int r1_r,int r2_l,int r2_r){
  int i,max_steps,j = 0 ;
  int steps[4] = { r1_l , r1_r , r2_l , r2_r };
  int polarity[4] = {0,0,0,0};

  /* clearing the mid read flag */
  mid_serial_read = false;
  
  /* determing max steps */
  max_steps = get_max_val(steps);

  /* determine poalrity of signals */
  determine_polarity(steps,polarity);

  /** turn voltage high and low to drive the stepper motor 
   *  break if serial avaiable 
   */
  time2 = micros();
  for(i=0;i<max_steps;i++){
    
    // turning pins HIGH 
    for(j=0;j<4;j++){
      if(abs(steps[j])>i){
        //turn on specific motor  PIN
        digitalWrite(motor_control_pins[j], HIGH);
        }   
     }


     // Check Serial and delay  
     serial_or_delay(motor_delay);
    
     // turning pins LOW 
    for(j=0;j<4;j++){
      if(abs(steps[j])>i){
        //turn off specific motor PIN
        //increment/decrement value of steps
        digitalWrite(motor_control_pins[j], LOW);
        motor_current[j] = motor_current[j] + polarity[j];
        }
     }
 
    // Check Serial and delay  
    serial_or_delay(after_motor_delay);
    
    // if flag raised break from loop
    if(mid_serial_read == true){
      break;
     }
  }
  
   time2 = micros()-time2;
   Serial.print("MOVE MOTOR TIMING:  ");
   Serial.println(time2);
}
///========================================================================
void serial_or_delay(int Delay){
    if(Serial.available() > 0){
//      Serial.println("MID SERIAL 2 ACTIVATE !!!");

      Serial_Read(lengths_angles,&safety);
      mid_serial_read = true;
     }
     else{
      delayMicroseconds(Delay);
     }
  }
///=========================================================================
void determine_polarity(int* steps,int* polarity){
  int j=0;
  for(j=0;j<4;j++){
     if(steps[j]<0){
      //counter clockwise

      //SET PIN FOR COUNTER CLOCKWISE HIGH
      digitalWrite(polarity_pins[j], HIGH);
      polarity[j] = counter_clockwise;
      }
      else{
      
      //SET PIN FOR COUNTER CLOCKWISE low
      digitalWrite(polarity_pins[j], LOW);
      polarity[j] = clockwise;
      }
      //Serial.println("Polarity");
      //Serial.println(polarity[j]);
   }
   //delay for polarity change
   delayMicroseconds(polarity_delay);
 }
//===========================================================================
void convert_to_steps(int* steps_to_move,float* lengths_angles,int* motor_current){
  
  steps_to_move[0] = length_to_steps(lengths_angles[0],motor_current[0]);
  steps_to_move[1] = angle_to_steps(lengths_angles[1],motor_current[1]);
  steps_to_move[2] = length_to_steps(lengths_angles[2],motor_current[2]);
  steps_to_move[3] = angle_to_steps(lengths_angles[3],motor_current[3]);

  Serial.println("Motor current");
  Serial.println(motor_current[0]);
  Serial.println(motor_current[1]);
  Serial.println(motor_current[2]);
  Serial.println(motor_current[3]);

  Serial.println("steps to move");
  Serial.println(steps_to_move[0]);
  Serial.println(steps_to_move[1]);
  Serial.println(steps_to_move[2]);
  Serial.println(steps_to_move[3]);
    
 }
//========================================================================
int get_max_val(int* steps){
  int max_steps;
  int i=0;
  
  max_steps = steps[0];
  for(i=0;i<4;i++){
    if(abs(steps[i]) > max_steps){
      max_steps = abs(steps[i]);
      }
    }
  return(max_steps);
}


