/*************************   FUNCTIONS ***************************
 * move_motor()
 * determine_polarity();
 * move_steps()
 * get_max_val()
 * convert_to_steps()
 */

 /*
  * Move motors to steps stored in the steps to move array
  */
void move_motor() {
  int i, max_steps, j = 0 ;
  int steps[4] = { steps_to_move[0] , steps_to_move[1] , steps_to_move[2] , steps_to_move[3] };
  int polarity[4] = {0, 0, 0, 0};

  /* clearing the mid read flag */
  mid_serial_read_flag = false;

  /* determing max steps */
  max_steps = get_max_val(steps);

  /* determine poalrity of signals */
  determine_polarity(steps, polarity);

  /** turn voltage high and low to drive the stepper motor
   *  break if serial avaiable
   */
  time2 = micros();
  for (i = 0; i < max_steps; i++) {
    // turning pins HIGH
    for (j = 0; j < 4; j++) {
      if (abs(steps[j]) > i) {
        if (steps[j] > 0 && digitalRead(sensor_pins[j][1])) {
          //turn on specific motor  PIN
          digitalWrite(motor_control_pins[j], HIGH);
          delayMicroseconds(between_motor_delay);
          motor_moved[j] = true;
        }
        else if (steps[j] < 0 && digitalRead(sensor_pins[j][0])) {
          //turn on specific motor  PIN
          digitalWrite(motor_control_pins[j], HIGH);
          delayMicroseconds(between_motor_delay);
          motor_moved[j] = true;
        }
        else if (!digitalRead(sensor_pins[j][1])) {
#ifdef SERIAL_PRINT
          if (j == 1 || j == 3) {
            Serial.println("ROTATION");
          }
#endif
          motor_current[j] = reset_array[j][1];
        }
        else if (!digitalRead(sensor_pins[j][0])) {
          motor_current[j] = reset_array[j][0];
        }
      }
    }


    // Check Serial and delay
    serial_or_delay(motor_delay);

    // turning pins LOW
    for (j = 0; j < 4; j++) {
      if (motor_moved[j] == true) {
        //turn off specific motor PIN
        //increment/decrement value of steps
        digitalWrite(motor_control_pins[j], LOW);
        motor_current[j] = motor_current[j] + polarity[j];
        delayMicroseconds(between_motor_delay);
        motor_moved[j] = false;
      }
    }

    // Check Serial and delay
    serial_or_delay(after_motor_delay);

    // if flag raised break from loop
    if (mid_serial_read_flag == true) {
      break;
    }
  }

  time2 = micros() - time2;
#ifdef SERIAL_PRINT
  Serial.print("MOVE MOTOR TIMING:  ");
  Serial.println(time2);
#endif

}
///========================================================================
void serial_or_delay(int Delay) {
  if (Serial.available() > 0) {

    //      Serial.println("MID SERIAL 2 ACTIVATE !!!");

    if (ReadSteps()) {
      mid_serial_read_flag = true;
    }
  }
  else {
    delayMicroseconds(Delay);
  }
}
///=========================================================================
void determine_polarity(int* steps, int* polarity) {
  int j = 0;
  for (j = 0; j < 4; j++) {
    if (steps[j] < 0) {
      //counter clockwise

      //SET PIN FOR COUNTER CLOCKWISE HIGH
      digitalWrite(polarity_pins[j], HIGH);
      polarity[j] = counter_clockwise;
    }
    else {

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
void convert_to_steps() {

  steps_to_move[0] = length_to_steps(lengths_angles[0], motor_current[0]);
  steps_to_move[1] = angle_to_steps(lengths_angles[1], motor_current[1]);
  steps_to_move[2] = length_to_steps(lengths_angles[2], motor_current[2]);
  steps_to_move[3] = angle_to_steps(lengths_angles[3], motor_current[3]);
#ifdef SERIAL_PRINT
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

#endif

}
//========================================================================
int get_max_val(int* steps) {
  int max_steps;
  int i = 0;

  max_steps = steps[0];
  for (i = 0; i < 4; i++) {
    if (abs(steps[i]) > max_steps) {
      max_steps = abs(steps[i]);
    }
  }
  return (max_steps);
}


