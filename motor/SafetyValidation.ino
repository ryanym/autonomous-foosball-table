void safety_broken(){
  /* disbale pins */
  
   digitalWrite(X_ENABLE_PIN    , HIGH);
   digitalWrite(Y_ENABLE_PIN    , HIGH);
   digitalWrite(Z_ENABLE_PIN    , HIGH);
   digitalWrite(E_ENABLE_PIN    , HIGH);
   digitalWrite(Q_ENABLE_PIN    , HIGH);  
#ifdef SERIAL_PRINT
   Serial.println("safety violated");
#endif

  safety = true;

  }

void stop_button_interupt(){
  safety_broken();
  }
