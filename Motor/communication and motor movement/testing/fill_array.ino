void separate_into_array(String incomingByte,float* lengths_angles,bool* safety){
  
  int i = 0 ; 
  int j = 0 ;
  int string_counter = 0;
  int array_count = 0;
  String append = "";
  
    for(i=0;i<num_receive;i++){
        for(j=0;j<100;j++){
          //detect for commas
          if(incomingByte[string_counter] == ','){
         
            //convert to integer add to move array
            if(array_count<4){
              lengths_angles[array_count] = 0;
              lengths_angles[array_count] = append.toFloat();
                         
            }

            if(array_count == 4){
              if(append[0] == 't' || append[0] == 'T'){
                *safety = true;
                }
              else if(append[0] == 'f' || append[0] == 'F'){
                *safety = false;
                safety_broken();
                }
            }
//TEMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP

            if(array_count == 5){
               motor_delay = append.toFloat();
            }
            
            if(array_count == 6){
               after_motor_delay = append.toFloat();
            }
            
            if(array_count == 7){
               polarity_delay = append.toFloat();
            }
            
//TEMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP 
            //Increment counters and reset append string
            array_count++;  
            string_counter++;
            append="";
            break;
           }
            
          //append characetr to existing string
          append = append + incomingByte[string_counter];
          string_counter++;          
          }
      }
  }


