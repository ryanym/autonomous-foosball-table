#define X_STEP_PIN         2 
#define X_DIR_PIN          5
#define X_ENABLE_PIN       8

#define Y_STEP_PIN         3
#define Y_DIR_PIN          6
#define Y_ENABLE_PIN       8

#define Z_STEP_PIN         4
#define Z_DIR_PIN          7
#define Z_ENABLE_PIN       8

/*The data to be sent should be comma delimited ex 4,5,6,7, the last comma is importatnt as well
 * When changing the number of receivevd varaibles make sure you change on the PC side
 * Program currently configred to do stuff with 4 vairables
 */
 
//four motors going from row1_linear,row1_rotational,row2_linear,row2_rotational
//max size is 32767 for each integer...do not go above this limit
int Move[4] = {0,0,0,0};

 //Safety is false but turns true if system needs to stop
bool Safety = false;
bool finishedRot = true;
 //number of data to be received
 //code must be changed as right now onyl the motor buffers are being filled
int num_receive = 5;

 //to signify if anything has entered serial
int Read = 0 ;

//linear Gear
int num_teeth = 30;
int spacing_teeth  = 0.360; 

//motor
int steps_rev = 200;
int counter = 0;
void setup() {
  // put your setup code here, to run once:
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




void loop() {
  
  Serial_Read(Move,&Safety);

  step(X_STEP_PIN,Move[0],1000);
  
  
}

int step(int motor, int steps, int delay){
  if(counter < steps){
    digitalWrite(motor, HIGH);
    delayMicroseconds(delay);
    digitalWrite(motor, LOW);
    delayMicroseconds(delay);
    counter++;    
  }
  return 1;
}







