#ifndef Barometric_Sensor
#define Barometric_Sensor

#include <math.h>
#include <Wire.h>
#include "BaroSensor.h"
#include <SPI.h>
#include <SD.h>

#include "Sensor.h"

class BarometricSensor : public Sensor {
public:
    boolean setup(void);
    void headers(File* f);
    void write(File* f);
    double getAltitude(double, double);

    double getTemperature();
    double getPressure();
    
};

extern BarometricSensor Barometric;

#endif
