#include "Arduino.h"
#include "DOFSensor.h"

DOFSensor::DOFSensor() : dof(MODE_I2C, 0x6B, 0x1D) {}

boolean DOFSensor::setup() {
  dof.begin();
}

void DOFSensor::headers(File* f) {
  f->print("ax,ay,az,gx,gy,gz,mx,my,mz,heading"); // accelerometer x, y, z, gyro x, y, z, mag x,y,z
}

void DOFSensor::write(File* f) {
  dof.readAccel();

  f->print(dof.calcAccel(dof.ax), 10);
  f->print(",");
  f->print(dof.calcAccel(dof.ay), 10);
  f->print(",");
  f->print(dof.calcAccel(dof.az), 10);
  f->print(",");
  dof.readGyro();
  f->print(dof.calcGyro(dof.gx), 10);
  f->print(",");
  f->print(dof.calcGyro(dof.gy), 10);
  f->print(",");
  f->print(dof.calcGyro(dof.gz), 10);
  f->print(",");
  dof.readMag();
  f->print(dof.calcMag(dof.mx), 10);
  f->print(",");
  f->print(dof.calcMag(dof.my), 10);
  f->print(",");
  f->print(dof.calcMag(dof.mz), 10);
  f->print(calcHeading(), 10);


  print_data();
}

void DOFSensor::print_data() {
  dof.readAccel();
  Serial.print(dof.calcAccel(dof.ax), 10);
  Serial.print(",");
  Serial.print(dof.calcAccel(dof.ay), 10);
  Serial.print(",");
  Serial.print(dof.calcAccel(dof.az), 10);
  Serial.print(",");
  dof.readGyro();
  Serial.print(dof.calcGyro(dof.gx), 10);
  Serial.print(",");
  Serial.print(dof.calcGyro(dof.gy), 10);
  Serial.print(",");
  Serial.print(dof.calcGyro(dof.gz), 10);
  Serial.print(",");
  dof.readMag();
  float heading = calcHeading();
  Serial.println(heading);

}
float DOFSensor::calcHeading() {
  // cacluate heading (from north) from Magetnometer data
  // DOES NOT WORK
  float heading = atan2(dof.my, dof.mx);
  heading += 1.15;

  if (heading < 0) {
    heading += 2 * PI;
    if (heading > 2 * PI);
    heading -= 2 * PI;
  }

  return (heading * (180 / PI));

}

DOFSensor DOF;
