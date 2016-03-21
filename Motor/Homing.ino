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
      if(digitalRead(sensor_pins[j]) && sensor_pins[j] != 0 ){
        //turn on specific motor  
          digitalWrite(motor_control_pins[j], HIGH);
        }    
     }

    delayMicroseconds(homing_delay);
    
     //turning LOW
    for(j=0;j<4;j+=2){
      if(digitalRead(sensor_pins[j]) && sensor_pins[j] != 0 ){
        digitalWrite(motor_control_pins[j], LOW);
       }
     }

     delayMicroseconds(homing_delay);
  }
  
  /* zero-in the current motors */
  for(j=0;j<4;j++){
    motor_current[j] = 0;
  }
}
