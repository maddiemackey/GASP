#ifndef Humidity_Sensor
#define Humidity_Sensor

#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include "SparkFunHTU21D.h"

#include "Sensor.h"

class HumiditySensor : public Sensor {
public:
    boolean setup();
    void headers(File* f);
    void write(File* f);
private:
    float getHumidity();
    float getTemperature();
    float getDewPoint();
    float getDewPoint(float temperature, float humidity);
    float getPressure();
    float getPressure(float temperature);
    HTU21D humiditySensor;
};

extern HumiditySensor Humidity;

#endif