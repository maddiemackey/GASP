#include "Arduino.h"
#include "HumiditySensor.h"

boolean HumiditySensor::setup() {
    humiditySensor.begin();
    pinMode(10, OUTPUT);
    return true;
}

void HumiditySensor::headers(File* f) {
    f->print("humidity,temperature,dewpoint");
}

void HumiditySensor::write(File* f) {
    f->print(getHumidity());
    f->print(",");
    f->print(getTemperature());
    f->print(",");
    f->print(getDewPoint());
}

float HumiditySensor::getHumidity() {
    return humiditySensor.readHumidity();
}

float HumiditySensor::getTemperature(){
    return humiditySensor.readTemperature();
}

float HumiditySensor::getDewPoint() {
    return getDewPoint(getTemperature(), getHumidity());
}

float HumiditySensor::getDewPoint(float temperature, float humidity){
    float dewPointTemperature = pow((humidity/100),(1/8)) * (112+0.9*temperature) + 0.1*temperature - 112;
    return dewPointTemperature;
}

float HumiditySensor::getPressure(){
    return getPressure(getTemperature());
}

float HumiditySensor::getPressure(float temperature){
  float partialPressure = pow(10,(8.1332 - (1762.39/(temperature + 235.66))));
  //Calculates partial pressure from sensor data
  return partialPressure;
}

HumiditySensor Humidity;