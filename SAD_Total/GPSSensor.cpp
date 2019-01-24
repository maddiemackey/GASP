#include "Arduino.h"
#include "GPSSensor.h"
boolean GPSSensor::setup() {
  //Serial.begin(9600);
  return true;
}

void GPSSensor::headers(File* f) {
  f->print("date,time,satellites,lat,lng,alt");
}

void GPSSensor::write(File* f) {
  f->print(gps.date.day());
  f->print("/");
  f->print(gps.date.month());
  f->print("/");
  f->print(gps.date.year());
  f->print(",");
  f->print(gps.time.hour());
  f->print(":");
  f->print(gps.time.minute());
  f->print(":");
  f->print(gps.time.second());
  f->print(":");
  f->print(gps.time.centisecond());
  f->print(",");
  f->print(gps.satellites.value(), 10);
  f->print(",");
  f->print(getLat(), 10);
  f->print(",");
  f->print(getLng(), 10);
  f->print(",");
  f->print(getAlt(), 10);

  print_data();
}

//If the serial port is available, return value of Latitude in degrees
double GPSSensor::getLat() {
  encodeSerial();
  return gps.location.lat();
}

//If the serial port is available and gps data has been updated, return value of Longitude in degrees
double GPSSensor::getLng() {
  encodeSerial();
  return gps.location.lng();
}

//If the serial port is available and gps data has been updated, return value of current timestamp in HH:MM:SS form or Hours, Minutes, Seconds
double GPSSensor::getTime() {
  encodeSerial();
  return gps.time.value();
}

//If the serial port is available and gps data has been updated, return value of Altitude in meters
double GPSSensor::getAlt() {
  encodeSerial();
  return gps.altitude.meters();
}

void GPSSensor::encodeSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    //Serial.print(c);
    gps.encode(c);
  }
}
void GPSSensor::print_data() {
  Serial.print(getLat(), 10);
  Serial.print(",");
  Serial.print(getLng(), 10);
  Serial.print(",");
  Serial.print(getAlt(), 10);
}


GPSSensor GPS;
