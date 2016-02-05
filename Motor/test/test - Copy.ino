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

<<<<<<< HEAD:Motor/test.ino
void setup() {  
=======
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


Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  pinMode(FAN_PIN , OUTPUT);
  pinMode(HEATER_0_PIN , OUTPUT);
  pinMode(HEATER_1_PIN , OUTPUT);
  pinMode(LED_PIN  , OUTPUT);
  
>>>>>>> origin/master:Motor/test/test.ino
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
