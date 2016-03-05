//takes in real linear lenght and current step postiion and converts to number of steps
int length_to_steps(float linear_length,int motor_current){
 //distance = 3.6cm * 30 teeth
 //need number of rotation first
 //200 steps per rotation
 float length_per_steps; 
 length_per_steps = (spacing_teeth * num_teeth) / linear_steps;
 float steps_needed = linear_length/length_per_steps - motor_current;
 
 return(steps_needed);
  }


