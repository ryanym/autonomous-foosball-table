int ReadSteps() {
  time_start  = micros();
  String content = "";

  //Read input strings and raise Read falg
  while (Serial.available() > 0 ) {
    content = Serial.readStringUntil('n');
    serial_read_flag = true;
  }

  //if flag riased dissect into propeer array
  //if only one data then probably for getting current steps or RESET
  if (serial_read_flag == 1) {
    if (strlen(content.c_str()) != 1) {
      for (int i = 0; i < 4; i++) {
        int index = content.indexOf(",");
        lengths_angles[i] = atol(content.substring(0, index).c_str());
        content = content.substring(index + 1);
      }
    }
    else {
      if ( content[0] == 'R') {
        wdt_enable(WDTO_15MS );
      }
      else {
        int time_start2 = micros();
        print_return_steps();
        int time_end = micros() - time_start2;
        int time_end2 = time_start2 - time_start;
#ifdef SERIAL_PRINT
        Serial.println(time_end);
        Serial.println(time_end2);
#endif
        delayMicroseconds(serial_motor_delay);
        serial_read_flag = 0;
        return (-1);
      }
    }
    //check safety flag
    //int index = content.indexOf(",");
    //if(content.substring(0,index)[0] == 't'){
    //safety_broken();
    //}

    time_elapsed = micros() - time_start;

#ifdef SERIAL_PRINT
    print_length_angles();
    Serial.print(" Serial timings  ");
    Serial.println(time_elapsed);
#endif
    serial_read_flag = 0;
  }
  return (1);
}


/********************** PRINT FUCNTIONS ***********************/

//Printing return steps
void print_return_steps() {
  Serial.print(motor_current[0]);
  Serial.print(",");
  Serial.print(motor_current[1]);
  Serial.print(",");
  Serial.print(motor_current[2]);
  Serial.print(",");
  Serial.println(motor_current[3]);
}

//Printing array lenght/angles contents
void print_length_angles() {
  Serial.println(lengths_angles[0]);
  Serial.println(lengths_angles[1]);
  Serial.println(lengths_angles[2]);
  Serial.println(lengths_angles[3]);
}

