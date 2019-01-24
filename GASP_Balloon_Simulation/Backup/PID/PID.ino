/* -------------------
 *  Control Algorithm 
 *  IT 2016 
 *  Andrew Wilkie, Maddie Mackey 
 ---------------------*/
// output pins
#define left 3 
#define right 9

unsigned long lastTime;
float Input, Output = 500; 
float Setpoint = 250; // Home GPS coordinates? 
float errSum, lastErr;

/* ---------PID Constants --------*/
float kp = 0.7;
float kd = 8;
float ki = 0.00001;

/*--------PID Algorithm Variables ---*/
unsigned long lastTime;
float Input, Output = 500; 
float Setpoint = 250; // Home GPS coordinates? 
float errSum, lastErr;

/*----- Other Variable ----*/ 
float longitude, latitude, altitude = 0 //GPS Variables


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Input = analogRead(); // some form of input from the edison. Bearing of the craft
  calculateAngle(); // recalculate the setpoint
  computePID(); // calculate the outputs. Might have several PID algoprithms running different things (eg. one for left, one for right)
  Move(Output);

}

void computePID()
{
  /*How long since we last calculated*/
  unsigned long now = millis();
  double deltaT = (double)(now - lastTime);

  /*Compute all the working error variables*/
  double error = Setpoint - Input;
  errSum += (error * deltaT);
  double dErr = (error - lastErr) / deltaT;

  /*Compute PID Output*/
  Output = kp * error + ki * errSum + kd * dErr;

  /*Remember some variables for next time*/
  lastErr = error;
  lastTime = now;
}

void calculateAngle() {
  /* calculate the angle the craft needs to turn to be facing home */
}

void Move(output) {
  Serial.println(output);
}
