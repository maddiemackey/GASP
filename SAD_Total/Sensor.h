#ifndef Sensor_h
#define Sensor_h

#include "Arduino.h"
#include <SD.h>
#include <Servo.h>

class Sensor {
public:
    virtual boolean setup(){};
    virtual void headers(File* f){};
    virtual void write(File* f){};
};

#endif
