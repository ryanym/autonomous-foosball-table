//r1_l = rotation linear
//assumption : motor rotates Clockwise when pin set high
//assumption : clokwise is for postive number of steps and counter is for negative
/*
 * move_motor()
 * get_max_val()
 * convert_to_steps()
 */
void move_motor(int r1_l,int r1_r,int r2_l,int r2_r){
  int i,max_steps,j = 0 ;
  int steps[4] = { r1_l , r1_r , r2_l , r2_r };
  int polarity[4] = {0,0,0,0};
  
  
   //determing maximum value
  max_steps = get_max_val(steps);

  //determine poalrity of signals
  for(j=0;j<3;j++){
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
   }
   

  //turn voltage high and low to drive the stepper motor
  for(i=0;i<=max_steps;i++){
    //turning HIGH
    for(j=0;j<3;j++){
      if(steps[j]<i){
        //turn on specific motor  PI
        digitalWrite(motor_pins[j], HIGH);
        }   
     }

    delayMicroseconds(motor_delay);
    
     //turning LOW
    for(j=0;j<3;j++){
      if(steps[j]<i){
        //turn off specific motor PIN
        //increment value of steps
        digitalWrite(motor_pins[j], LOW);
        motor_current[j] = motor_current[j] + polarity[j];
        }
     }
  }

  //0 ing all the movements so movements do not repeat
  for(i=0;i<4;i++){
    Move[i] = 0;
  }
}

//===========================================================================
void convert_to_steps(int* steps_to_move,int* lengths_angles,int* motor_current){
  int i = 0 ;
  for(i=0;i<4;i++){
    steps_to_move[i] = length_to_steps(lengths_angles[i],motor_current[i]);
  }
 }
//========================================================================
int get_max_val(int* steps){
  int max_steps;
  int i=0;
  
  max_steps = steps[0];
  for(i=0;i<4;i++){
    if(steps[i] > max_steps){
      max_steps = steps[i];
      }
    }
  return(max_steps);
}


