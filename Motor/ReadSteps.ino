void ReadSteps(float* lengths_angles,bool* safety){
  time_start  = micros();
  String content = "";

  //Read input strings and raise Read falg
  while(Serial.available() > 0 ){
    content = Serial.readStringUntil('n');
    Read = 1;  
    serial_read = true; 
  }

 //if flag riased dissect into propeer array
  if(Read == 1){
    for(int i = 0; i < 4; i++){
      int index = content.indexOf(","); 
      lengths_angles[i] = atol(content.substring(0,index).c_str()); 
      content = content.substring(index+1); 
    }

    //check safety flag
    //int index = content.indexOf(","); 
    //if(content.substring(0,index)[0] == 't'){
      //safety_broken();
      //}
  
    time_end = micros();
    time_elapsed = time_end - time_start;
    Serial.print("SERIAL TIMINGS");
    Serial.println(time_elapsed);
    Serial.println(lengths_angles[0]);
    Serial.println(lengths_angles[1]);
    Serial.println(lengths_angles[2]);
    Serial.println(lengths_angles[3]);
    

    Read = 0;
  }
}
