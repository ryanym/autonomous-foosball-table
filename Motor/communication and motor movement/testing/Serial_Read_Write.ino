//takes in a pointer to an array which is 4 bytes long
//linear lenghts should be in cm
void Serial_Read(int* lengths_angles,bool* safety){
  String incomingByte ="" ;
  
  while(Serial.available() > 0) {
    //Time testing
    time_start  = micros();
    
    //these delays are important so data keeps on being read
            delay(1);
            // read the incoming byte:\
            int inChar = Serial.read();   
            incomingByte += (char)inChar;
            
            Read = 1;  
            serial_read = true;         
            delay(1);
    }

  //if Serial read then print out return string
  if(Read  == 1){
    
    //printing array after and fills the Move array with the 4 received integers
    separate_into_array(incomingByte,lengths_angles,safety);

    //sending data back
    Serial.println(lengths_angles[0]);
    Serial.println(lengths_angles[1]);
    Serial.println(lengths_angles[2]);
    Serial.println(lengths_angles[3]);
    
  
    Read = 0;
    incomingByte = "";

    //Serial timing 16Mhz - 4 us resolution
    time_end = micros();
    time_elapsed = time_end - time_start;
    Serial.print("SERIAL TIMINGS");
    Serial.println(time_elapsed);
  }
  
}



