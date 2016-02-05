//takes in real angle and converts to number of steps
int length_to_steps(float linear_length){
 //distance = 360mm * 30 teeth
 //need number of rotation first
 //200 steps per rotation
 float num_rotations;

 num_rotations = linear_length / (spacing_teeth * num_teeth);
 return((int)stes_rev*10 / num_rotations*10);
  }
