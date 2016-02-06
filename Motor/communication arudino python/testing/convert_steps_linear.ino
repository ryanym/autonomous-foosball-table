//takes in real linear lenght and current step postiion and converts to number of steps
int length_to_steps(float linear_length,int motor_current){
 //distance = 360mm * 30 teeth
 //need number of rotation first
 //200 steps per rotation
 float num_rotations;

 num_rotations = linear_length / (spacing_teeth * num_teeth);
 int steps_needed = (linear_steps * 10 / (num_rotations * 10)) - motor_current;
 return(steps_needed);
  }
