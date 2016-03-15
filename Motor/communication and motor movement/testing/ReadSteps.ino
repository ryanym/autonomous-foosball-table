void ReadSteps(int* lengths_angles,bool* safety){
  time_start  = micros();
  String content = "";
  while(Serial.available() > 0 ){
    content = Serial.readString();
  }
  for(int i = 0; i < 4; i++){
    int index = content.indexOf(","); 
    lengths_angles[i] = atol(content.substring(0,index).c_str()); 
    content = content.substring(index+1); 
  }
  //  need to assign safety bit to something here rym

  time_end = micros();
  time_elapsed = time_end - time_start;
//  Serial.print("SERIAL TIMINGS");
//  Serial.println(time_elapsed);
//  Serial.println(lengths_angles[0]);
//  Serial.println(lengths_angles[1]);
//  Serial.println(lengths_angles[2]);
//  Serial.println(lengths_angles[3]);
}
