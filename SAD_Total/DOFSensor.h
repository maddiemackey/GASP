#ifndef AccelGyro_Sensor
#define AccelGyro_Sensor
#include <SPI.h> // Included for SFE_LSM9DS0 library
#include <Wire.h>
#include "SFE_LSM9DS0.h"
#include <SD.h>

#include "Sensor.h"

class DOFSensor : public Sensor {
public:
    DOFSensor();
    boolean setup(void);
    void headers(File* f);
    void write(File* f);
    void print_data();
    float calcHeading();
private:
    LSM9DS0 dof;
};

extern DOFSensor DOF;

#endif
