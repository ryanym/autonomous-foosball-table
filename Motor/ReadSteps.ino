int ReadSteps(float* lengths_angles,bool* safety){
  time_start  = micros();
  String content = "";
  
  //Read input strings and raise Read falg
  while(Serial.available() > 0 ){
    content = Serial.readStringUntil('n');
    Read = 1;  
    serial_read = true; 
  }

 //if flag riased dissect into propeer array
 //if only one data then probably for getting current steps
  if(Read == 1){
    if(strlen(content.c_str()) != 1){
      for(int i = 0; i < 4; i++){
        int index = content.indexOf(","); 
        lengths_angles[i] = atol(content.substring(0,index).c_str()); 
        content = content.substring(index+1); 
      }
    }
    else{
      if(content[0] == 'h'){
#ifdef SERIAL_PRINT
          Serial.println("HOME");
#endif
        homing_flag = true;
        }
      else{
        int time_start2 = micros();
        Serial.print(motor_current[0]);
        Serial.print(",");
        Serial.print(motor_current[1]);
        Serial.print(",");
        Serial.print(motor_current[2]);
        Serial.print(",");
        Serial.println(motor_current[3]);
        int time_end = micros()-time_start2;
        int time_end2 = time_start2-time_start;
  #ifdef SERIAL_PRINT
        Serial.println(time_end);
        Serial.println(time_end2);
  #endif
        serial_read = false;    //for motor move so not needed
        Read = 0;
        return(-1);
      }
    }
    //check safety flag
    //int index = content.indexOf(","); 
    //if(content.substring(0,index)[0] == 't'){
      //safety_broken();
      //}
  
    time_elapsed = micros() - time_start;
    time_start = micros();

#ifdef SERIAL_PRINT
    Serial.println(lengths_angles[0]);
    Serial.println(lengths_angles[1]);
    Serial.println(lengths_angles[2]);
    Serial.println(lengths_angles[3]);
#endif

    time_elapsed = micros() - time_start;
  
#ifdef SERIAL_PRINT
    Serial.print(" PRINT TIMINGS   ");
    Serial.println(time_elapsed);
#endif
    Read = 0;
  }
  return(1);
}
