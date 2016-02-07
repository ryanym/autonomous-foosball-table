//takes in a pointer to an array which is 4 bytes long
//linear lenghts should be in cm
void Serial_Read(int* Move,bool* Safety){
  String incomingByte ="" ;
  
  while(Serial.available() > 0) {
    //these delays are important so data keeps on being read
            delay(1);
            // read the incoming byte:\
            int inChar = Serial.read();   
            incomingByte += (char)inChar;
            
            Read = 1;           
            delay(1);
            
    }

  //if Serial read then print out return string
  if(Read  == 1){
    
    //printing array after and fills the Move array with the 4 received integers
    separate_into_array(incomingByte,Move,Safety);

    //sending data back
    Serial.println(Move[0] + 3);
    Serial.println(Move[1]);
    Serial.println(Move[2]);
    Serial.println(Move[3]);
    
    counter = 0;
    Read = 0;
    incomingByte = "";
  }

}



