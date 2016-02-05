#define X_STEP_PIN         2 
#define X_DIR_PIN          5
#define X_ENABLE_PIN       8

#define Y_STEP_PIN         3
#define Y_DIR_PIN          6
#define Y_ENABLE_PIN       8

#define Z_STEP_PIN         4
#define Z_DIR_PIN          7
#define Z_ENABLE_PIN       8


int val = 0; 

void setup() {  
  pinMode(X_STEP_PIN  , OUTPUT);
  pinMode(X_DIR_PIN    , OUTPUT);
  pinMode(X_ENABLE_PIN    , OUTPUT);
  
  pinMode(Y_STEP_PIN  , OUTPUT);
  pinMode(Y_DIR_PIN    , OUTPUT);
  pinMode(Y_ENABLE_PIN    , OUTPUT);
  
  pinMode(Z_STEP_PIN  , OUTPUT);
  pinMode(Z_DIR_PIN    , OUTPUT);
  pinMode(Z_ENABLE_PIN    , OUTPUT);
  
    digitalWrite(X_ENABLE_PIN    , LOW);
    digitalWrite(Y_ENABLE_PIN    , LOW);
    digitalWrite(Z_ENABLE_PIN    , LOW);
}



int count=0;

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


  //if(count<200){
    digitalWrite(X_STEP_PIN    , HIGH);
    digitalWrite(Y_STEP_PIN    , HIGH);
    digitalWrite(Z_STEP_PIN    , HIGH);
    
    //delay(10);
    delayMicroseconds(400);
    
    digitalWrite(X_STEP_PIN    , LOW);
    digitalWrite(Y_STEP_PIN    , LOW);
    digitalWrite(Z_STEP_PIN    , LOW);
    delayMicroseconds(400);
    //delay(10);
    count++;
  //}
    //counter++;
    //Serial.println(counter);
}
