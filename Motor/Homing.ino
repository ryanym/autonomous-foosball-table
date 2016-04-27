void homing(int* motor_current){
  int j,i = 0;
  int max_steps = 400;
  
  /* make all the motors go counter clockwise */ 
  for(j=0;j<4;j++){
    digitalWrite(polarity_pins[j], HIGH);
  }
  
  //polarity change delay
  delayMicroseconds(polarity_delay);
  
  /* turn voltage high and low to drive the stepper motor */
  for(i=0;i<max_steps;i++){
    //turning HIGH
    for(j=0;j<4;j++){
     //if snesor not triggered then change polarity and is defined
      if(digitalRead(sensor_pins[j][0]) && sensor_pins[j][0] != 0 ){
        //turn on specific motor  
          digitalWrite(motor_control_pins[j], HIGH);
        }    
     }

    delayMicroseconds(homing_delay);
    
     //turning LOW
    for(j=0;j<4;j++){
      if(digitalRead(sensor_pins[j][0]) && sensor_pins[j][0] != 0 ){
        digitalWrite(motor_control_pins[j], LOW);
       }
     }

     delayMicroseconds(homing_delay);
  }
  
  //Reset rotation
   move_motor(0,-motor_current[1],0,-motor_current[3]);
   
  /* zero-in the current motors */
  for(j=0;j<4;j++){
    motor_current[j] = reset_array[j][0];
    lengths_angles[j] = 0;
  }
}
