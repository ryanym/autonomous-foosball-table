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
  
   digitalWrite(X_ENABLE_PIN    , LOW);
   digitalWrite(Y_ENABLE_PIN    , LOW);
   digitalWrite(Z_ENABLE_PIN    , LOW);
   digitalWrite(E_ENABLE_PIN    , LOW);
   digitalWrite(Q_ENABLE_PIN    , LOW);
  
}


