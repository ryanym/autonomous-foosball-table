//takes in a pointer to an array which is 4 bytes long
//linear lenghts should be in cm
void Serial_Read(float* lengths_angles,bool* safety){
  String incomingByte ="" ;
  time3 = micros();
  /*while(Serial.available() > 0) {
   // Time testing
    //time_start  = micros();
    
    //these delays are important so data keeps on being read
            delayMicroseconds(500);
            // read the incoming byte:\
            int inChar = Serial.read();   
            incomingByte += (char)inChar;
            
            Read = 1;  
            serial_read = true;         
            delayMicroseconds(500);
    }*/
    
    while(Serial.available() > 0) {
    
    //these delays are important so data keeps on being read
            // read the incoming byte:\
            
            incomingByte = Serial.readStringUntil('\n');
            
            Read = 1;  
            serial_read = true;             
    }
    time3 = micros() - time3;
  
  //if Serial read then print out return string
  if(Read  == 1){
    time1 = micros();
    //printing array after and fills the Move array with the 4 received integers
    separate_into_array(incomingByte,lengths_angles,safety);
    time1 = micros() - time1;
    Serial.print("Timing  ARRAY   ");
    Serial.println(time1);
    Serial.print("TIMING get data   ");
    Serial.println(time3);
    
    //sending data back
    Serial.println(lengths_angles[0]);
    Serial.println(lengths_angles[1]);
    Serial.println(lengths_angles[2]);
    Serial.println(lengths_angles[3]);
    
    Read = 0;
    incomingByte = "";

    //Serial timing 16Mhz - 4 us resolution - 600 us
  }
  
}



