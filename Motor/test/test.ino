#define X_STEP_PIN         2 
#define X_DIR_PIN          5
#define X_ENABLE_PIN       8

#define Y_STEP_PIN         3
#define Y_DIR_PIN          6
#define Y_ENABLE_PIN       8

#define Z_STEP_PIN         4
#define Z_DIR_PIN          7
#define Z_ENABLE_PIN       8


void setup() {
  Serial.begin(9600);
  Serial.print("RESET");
 
  
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


String steps; 
void loop () {  
//  while(Serial.available()) {
//    //these delays are important so data keeps on being read
//    delay(1);
//    // read the incoming byte:\
//    steps = Serial.readString ();
//    delay(1);
//    
//    Serial.println(steps);  
//  }
//  //step(X_STEP_PIN,steps,400);
//  //steps = 0;
}



int step(int motor, int steps, int delay){
  int counter = 0;
  if(counter < steps){
    digitalWrite(motor, HIGH);
    delayMicroseconds(delay);
    digitalWrite(motor, LOW);
    delayMicroseconds(delay);
    counter++;    
  }
  return 1;
}


