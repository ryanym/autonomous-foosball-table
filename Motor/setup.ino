#include "pin_def.h"

void enable_pins(){
  pinMode(LED_PIN  , OUTPUT);
  
  pinMode(X_STEP_PIN  , OUTPUT);
  pinMode(X_DIR_PIN    , OUTPUT);
  pinMode(X_ENABLE_PIN    , OUTPUT);
  pinMode(X_MIN_PIN      , INPUT);
  pinMode(X_MAX_PIN     , INPUT);
  
  pinMode(Y_STEP_PIN  , OUTPUT);
  pinMode(Y_DIR_PIN    , OUTPUT);
  pinMode(Y_ENABLE_PIN    , OUTPUT);
  pinMode(Y_MIN_PIN      , INPUT);
  pinMode(Y_MAX_PIN    , INPUT);
  
  pinMode(Z_STEP_PIN  , OUTPUT);
  pinMode(Z_DIR_PIN    , OUTPUT);
  pinMode(Z_ENABLE_PIN    , OUTPUT);
  pinMode(Z_MIN_PIN    , INPUT);
  pinMode(Z_MAX_PIN    , INPUT);
  
  pinMode(E_STEP_PIN  , OUTPUT);
  pinMode(E_DIR_PIN    , OUTPUT);
  pinMode(E_ENABLE_PIN    , OUTPUT);
  
  pinMode(Q_STEP_PIN  , OUTPUT);
  pinMode(Q_DIR_PIN    , OUTPUT);
  pinMode(Q_ENABLE_PIN    , OUTPUT);

  pinMode(FAN_PIN, OUTPUT);
  
   digitalWrite(FAN_PIN, HIGH); 
   digitalWrite(X_ENABLE_PIN    , LOW);
   digitalWrite(Y_ENABLE_PIN    , LOW);
   digitalWrite(Z_ENABLE_PIN    , LOW);
   digitalWrite(E_ENABLE_PIN    , LOW);
   digitalWrite(Q_ENABLE_PIN    , LOW);
  
}

void serial_config(){
  Serial.begin(baudrate);
#ifdef SERIAL_PRINT
  Serial.print("RESET");
#endif
  }


