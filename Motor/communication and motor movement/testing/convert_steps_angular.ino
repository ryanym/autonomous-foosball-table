//takes in real angle in degrees and current step postion and converts to number of steps
int angle_to_steps(float angle,int motor_current){
 //200 steps per rotation
 float steps = (angle * rotational_steps) /  (360) - motor_current;
 return((int)steps);
  }


