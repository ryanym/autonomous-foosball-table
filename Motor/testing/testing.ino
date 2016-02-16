#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN           2

#define Y_STEP_PIN         60
#define Y_DIR_PIN          61
#define Y_ENABLE_PIN       56
#define Y_MIN_PIN          14
#define Y_MAX_PIN          15

#define Z_STEP_PIN         46
#define Z_DIR_PIN          48
#define Z_ENABLE_PIN       62
#define Z_MIN_PIN          18
#define Z_MAX_PIN          19

#define E_STEP_PIN         26
#define E_DIR_PIN          28
#define E_ENABLE_PIN       24

#define Q_STEP_PIN         36
#define Q_DIR_PIN          34
#define Q_ENABLE_PIN       30

#define SDPOWER            -1
#define SDSS               53
#define LED_PIN            13

#define FAN_PIN            9

#define PS_ON_PIN          12
#define KILL_PIN           -1

#define HEATER_0_PIN       10
#define HEATER_1_PIN       8
#define TEMP_0_PIN          13   // ANALOG NUMBERING
#define TEMP_1_PIN          14   // ANALOG NUMBERING

int val = 0; 

void setup() {
  pinMode(X_MIN_PIN , INPUT);
  pinMode(FAN_PIN , OUTPUT);
  pinMode(HEATER_0_PIN , OUTPUT);
  pinMode(HEATER_1_PIN , OUTPUT);
  pinMode(LED_PIN  , OUTPUT);
  
  pinMode(X_STEP_PIN  , OUTPUT);
  pinMode(X_DIR_PIN    , OUTPUT);
  pinMode(X_ENABLE_PIN    , OUTPUT);
  
  pinMode(Y_STEP_PIN  , OUTPUT);
  pinMode(Y_DIR_PIN    , OUTPUT);
  pinMode(Y_ENABLE_PIN    , OUTPUT);
  
  pinMode(Z_STEP_PIN  , OUTPUT);
  pinMode(Z_DIR_PIN    , OUTPUT);
  pinMode(Z_ENABLE_PIN    , OUTPUT);
  
  pinMode(E_STEP_PIN  , OUTPUT);
  pinMode(E_DIR_PIN    , OUTPUT);
  pinMode(E_ENABLE_PIN    , OUTPUT);
  
  pinMode(Q_STEP_PIN  , OUTPUT);
  pinMode(Q_DIR_PIN    , OUTPUT);
  pinMode(Q_ENABLE_PIN    , OUTPUT);
  
   digitalWrite(X_ENABLE_PIN    , LOW);
    digitalWrite(Y_ENABLE_PIN    , LOW);
    digitalWrite(Z_ENABLE_PIN    , LOW);
    digitalWrite(E_ENABLE_PIN    , LOW);
    digitalWrite(Q_ENABLE_PIN    , LOW);
}



unsigned long count=0;

void loop () {
  /*
  val = digitalRead(X_MIN_PIN);

  digitalWrite(LED_PIN, val);

  
  if(val ==0){
  digitalWrite(X_ENABLE_PIN,HIGH);
  }else{
  digitalWrite(X_ENABLE_PIN, LOW);
  }
  */
  
  /*
  if (millis() %1000 <500) 
    digitalWrite(LED_PIN, HIGH);
  else
   digitalWrite(LED_PIN, LOW);
  */
  
  
//  if ( %10000 <5000) {
//    digitalWrite(X_DIR_PIN    , HIGH);
//    digitalWrite(Y_DIR_PIN    , LOW);
//    /*
//    digitalWrite(Z_DIR_PIN    , HIGH);
//    digitalWrite(E_DIR_PIN    , HIGH);
//    digitalWrite(Q_DIR_PIN    , HIGH);
//    */
//  }
//  else {
//    digitalWrite(X_DIR_PIN    , LOW);
//    digitalWrite(Y_DIR_PIN    , HIGH);
//    /*
//    digitalWrite(Z_DIR_PIN    , LOW);
//    digitalWrite(E_DIR_PIN    , LOW);
//    digitalWrite(Q_DIR_PIN    , LOW);
//    */
//  }
//  

   
    if(count%200 < 100){
      digitalWrite(X_DIR_PIN    , LOW);
      digitalWrite(Y_DIR_PIN    , LOW);
      digitalWrite(Z_DIR_PIN    , LOW);
      digitalWrite(E_DIR_PIN    , LOW);
      digitalWrite(Q_DIR_PIN    , LOW);
    }
      
    else{
      digitalWrite(X_DIR_PIN    , HIGH);
      digitalWrite(Y_DIR_PIN    , HIGH);
      digitalWrite(Z_DIR_PIN    , HIGH);
      digitalWrite(E_DIR_PIN    , HIGH);
      digitalWrite(Q_DIR_PIN    , HIGH);  
    }

    if(count%100 == 0){
          delayMicroseconds(2000);
    }
    count++;
    if(count == 20000){
      count=0;
      delayMicroseconds(2000);
    }

    
    digitalWrite(X_STEP_PIN    , HIGH);
    digitalWrite(Y_STEP_PIN    , HIGH);
    
    digitalWrite(Z_STEP_PIN    , HIGH);
    digitalWrite(E_STEP_PIN    , HIGH);
    digitalWrite(Q_STEP_PIN    , HIGH); 
    
    //delay(1);
    delayMicroseconds(1000);
    digitalWrite(X_STEP_PIN    , LOW);
    digitalWrite(Y_STEP_PIN    , LOW);
    digitalWrite(Z_STEP_PIN    , LOW);
    digitalWrite(E_STEP_PIN    , LOW);
    digitalWrite(Q_STEP_PIN    , LOW);  
    //delay(1);


    //counter++;
    //Serial.println(counter);
}