//Libraries
#include "Sensor.h"

#include "DOFSensor.h"
#include "BarometricSensor.h"
#include "GPSSensor.h"
#include "HumiditySensor.h"


//Define the outputs
//PWM0=3, PWM1=5, PWM2=9, PWM3=11
Servo myservo;
#define Buzzer 3
#define Led1 5
#define servo 11
#define para 9

//Power variables
#define currentPower 100
#define powerCritical 10

//PID Constants
#define _speed 10

#define kp 1
#define kd 0
#define ki 0

//PID Varibles
int current_time = 0;
float d_time = 0;
float error = 0;
float error_sum = 0;
float d_error = 0;
float last_error = 0;
float prev_time = 0;
char output = 0;

float setpoint = 0;
float _input = 0;

//Home base location
float home_lat = 0;
float home_lng = 0;
float home_lat2 = home_lat; 
float home_lng2 = home_lng; 
float home_alt = 0;

// Steering variables
float theta = 0;
float yaw = 0;
float alt;
double alt2;

//dummy variables
bool descending;
byte counter = 0;


//Sensor initialisation
#define NUM_SENSORS 3
Sensor* sensors[] = {&GPS, &DOF, &Barometric/*, &Humidity*/}; // gps is first to that timestamp may be the first column

GPSSensor gps;
DOFSensor dof;
BarometricSensor baro;

char file[12];

void setup() {
  Serial.begin(115200); // start serial

  // Define and reset servo
  myservo.attach(servo);
  myservo.write(0);

  // set pwm outputs
  pinMode(Buzzer, OUTPUT);
  pinMode(Led1, OUTPUT);
  pinMode(para, OUTPUT);
  pinMode(servo, OUTPUT);

  // check SD card
  if (!SD.begin(4)) {
    Serial.println("Could not open SD card.");
    while (!SD.begin(4)) {
      delay(1000);
      Serial.println("SD Error");
      servoTest();
      //tone(Buzzer, 50);
    }
  }

  //Create Logging file
  for (int i = 0; ; i++) {
    sprintf(file, "gasp%d.csv", i);
    if (!SD.exists(file)) {
      break;
    } else {
      Serial.print(file);
      Serial.println(" exists. Trying next file.");
    }
  } // always ensure a new file is used
  Serial.print("Using file ");
  Serial.print(file);
  Serial.println(".");
  File f = SD.open(file, FILE_WRITE);
  if (f == NULL) {
    Serial.println("Could not open file.");
    while (f == NULL) {
      delay(1000);
      Serial.println("File Error");
      //digitalWrite(Led1, HIGH);
      //tone(Buzzer, 50);
    }
  }

  // Check sensors
  for (int i = 0; i < NUM_SENSORS; i++) {
    Serial.print("Loading sensor ");
    Serial.print(i);
    Serial.print("... ");
    Sensor* sensor = sensors[i];
    if (!sensor->setup()) {
      Serial.println("error.");
      while (!sensor->setup()) { // check the sesnor for errors
        delay(1000);
        Serial.println("Sensor Error");
        //digitalWrite(Led1, HIGH);
        //tone(Buzzer, 50);

      }
    }
    Serial.println("success.");
  }

  // write sensor output headers to file
  File* fh = &f;
  fh->print("millis,");
  for (int i = 0; i < NUM_SENSORS; i++) { // print column headers
    sensors[i]->headers(fh);
    if (i != NUM_SENSORS - 1) {
      fh->print(",");
    }
  }

  // save the file
  f.println();
  f.flush();
  f.close();

  //test Outputs. signal to everyone that the payload is ready
  Serial.println("Testing Controls");
  //beacon();
  servoTest();

  delay(1000);
  Serial.println("READY");

}

void loop() {

  // open file
  File f = SD.open(file, FILE_WRITE);
  if (f == NULL) {
    Serial.println("Could not open file.");
    while (f == NULL) {
      delay(1000);
      Serial.println("File Error");

    }
  }

  File* fh = &f; // define file

  current_time = millis(); // check time since board has been on
  descending = check_descent(); // check whether payload descending

  //print sesnor outputs
  Serial.print("Printing row... ");
  Serial.print(current_time);
  Serial.print(",");
  fh->print(millis());
  fh->print(",");
  for (int i = 0; i < NUM_SENSORS; i++) { // print rows of data
    //Serial.print(i);
    sensors[i]->write(fh);
    if (i != NUM_SENSORS - 1) {
      fh->print(",");
      Serial.print(",");


    }
    //Serial.print(", ");
    //Serial.print(i);
  }
  Serial.println("done.");

  //

  if (descending) {
    alt = gps.getAlt(); // check altitude
    alt2 = baro.getAltitude(baro.getPressure(), baro.getTemperature());
    if (((alt - alt2) > 2000) || ((alt - alt2) < -2000)) {
      if ((alt2 < 29000) && (counter <= 2)) { //deploy parachute
        //deployParachute();
        counter++;
      }
      if (alt2 < 100) { //begin rudder control
        //rudderFunction();
      }
    }
    else {
      if ((alt < 29000) && (counter <= 2)) { //deploy parachute
        //deployParachute();
        counter++;
      }
      if (alt < 100) { //begin rudder control
        //rudderFunction();
      }
    }
  }

  f.println();
  f.flush();
  f.close();
  rudderFunction(); 
  delay(50); // wait then loop around
}

void beacon() {
  // flash a light and make a noise (used to locate payload in a field)
  byte dummy_var = 0;

  //Serial.println("Beacon");
  while (dummy_var < 2) {
    tone(Buzzer, 50);
    digitalWrite(Led1, HIGH);
    delay(200);
    noTone(Buzzer);
    digitalWrite(Led1, LOW);
    delay(200);
    tone(Buzzer, 50);
    digitalWrite(Led1, HIGH);
    delay(200);
    noTone(Buzzer);
    digitalWrite(Led1, LOW);
    delay(500);
    counter++;
    //Serial.println(counter);
  }

}

void servoTest()
{
  //test servo with sweep
  int pos = 0;

  for (pos = 0; pos < 180; pos += 1) // goes from 0 degrees to 180 degrees
  { // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 1; pos -= 1) // goes from 180 degrees to 0 degrees
  {
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

void rudderFunction() {
  //Steers the payload to desired direction (home)

  yaw = dof.calcHeading(); //takes current direction

  correctHome; 

  //if the GPS isn't returning an error: 
  if (gps.getLng() != 0){
    theta = compute_theta(gps.getLng(), gps.getLat(), home_lng2, home_lat2); //calculates angle to home
    current_time = millis();
  
    output = computePID(); //calculates output for servo
    //saves battery life by not rewriting to the servo if the output is the same
    if (yaw != output) {
      //maps the output so that it accounts for the inverted position of the servo
      output = output % 180;
      output = map(output, -90, 90, 135, 45); 
      myservo.write(output);
    }
    Serial.print("Rudder output: ");
    Serial.println(output);
  }
  //if the GPS isn't working, set the rudder to spiral 
  else{
    myservo.write(45);
  }
}


float computePID() {
  // calculates the PID output for the rudder
  //Proportional: 
  d_time = current_time - prev_time;
  error =  theta - yaw; //calculates difference between direction its facing and direction we want it to face

  //Integral: 
  error_sum = (error * d_time); //accumulative error

  if (d_time == 0) {
    d_time = 1;
  }

  //Derivative: 
  d_error = (last_error - error) / d_time;

  output = (kp * error + kd * d_error + ki * error_sum);

  //updates values for previous loop 
  last_error = error;
  prev_time = current_time;

  return (output);
}

float compute_theta(float x, float y, float home_x, float home_y) {
  //gets the difference in direction (angle) between the balloon's location and home's location
  float d_x = x - home_x;
  float d_y = y - home_y;

  //distance from home
  //float dist_to_home = sqrt((d_y*d_y)+(d_x*d_x));

  //calculate the angle (in Radians)
  theta = atan(d_y / d_x);
  //convert the angle from radians to degrees
  theta = (theta * 4068) / 71;
  
  return (theta);
}

float correctHome(){
  //calculates drift and corrects desired location for it 
  
  //lat = x
  //long = y
  
  //GRAPH PRESET VALUES (taken from drift simulation)
  float lat_linear_max = ((-33.8415)- (-33.5152));
  float lat_a_linear_max = 17657;
  float long_linear_max = (146.262 - 146.537);
  float long_a_linear_max = 18954;
 
  //variables
  float m_long;
  float m_lat; 
  float lat_drift;
  float long_drift; 

  float alt = gps.getAlt();
  
  //finds current drift (co-ordinates against altitude)
  //LATITUDE
  if (alt <= lat_a_linear_max){
    m_lat = lat_linear_max/lat_a_linear_max;
    lat_drift = m_lat * alt;
  }
  if (alt > lat_a_linear_max){
    lat_drift = -33.5233;
  }
  //LONGITUDE
  if (alt <= long_a_linear_max){
    m_long = long_linear_max/long_a_linear_max;
    long_drift = m_long * alt;
  }
  if (alt > long_a_linear_max){
    long_drift = 146.557; 
  }

  //corrects home for drift 
  home_lat2 = home_lat - lat_drift; 
  home_lng2 = home_lng - long_drift; 
}

boolean check_descent() {
  // return a value depending on whether the payload
  // is descending or not
  
  double alt2_intitial = baro.getAltitude(baro.getPressure(), baro.getTemperature()); // barometric altitude
  float initialAlt = gps.getAlt(); // gps altitude

  delay(500);

  double alt2_final = baro.getAltitude(baro.getPressure(), baro.getTemperature());
  float secondAlt = gps.getAlt();

  float difference = initialAlt - secondAlt;
  float difference2 = alt2_intitial - alt2_final;

  if ((difference < 0) or (difference2 < 0)) { // check both gps and barometer (GPS has possibility to fail at high altitudes)
    return (true);
  }
  else {
    return (false);
  }
}

void deployParachute() {
  // set the pins high to disconnect the balloon from the parachute
  // deploying the parachute
  digitalWrite(para, HIGH);
  delay(6000);
  digitalWrite(para, LOW); // turn the pin off to not melt anything else
}



