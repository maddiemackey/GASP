#include "Arduino.h"
#include "BarometricSensor.h"
boolean BarometricSensor::setup() {
    BaroSensor.begin();
    //Serial.begin(9600);
    return BaroSensor.isOK();
}

void BarometricSensor::headers(File* f) {
    f->print("altitude,pressure,temp");
}

void BarometricSensor::write(File* f) {
    double pressure = getPressure();
    double temp = getTemperature();
    f->print(getAltitude(pressure, temp), 10);
    f->print(",");
    f->print(pressure, 10);    
    f->print(",");
    f->print(temp, 10);
    Serial.print(getAltitude(pressure, temp), 10);
    Serial.print(",");
    Serial.print(pressure, 10);
    Serial.print(",");
    Serial.print(temp,10);
}

double BarometricSensor::getTemperature() {
    return BaroSensor.getTemperature();
}

double BarometricSensor::getPressure() {
    return BaroSensor.getPressure();
}

#define R 8.31432 //Universal pressure constant in Newton-metres per molars*kelvin.
#define g 9.80665 //Gravitational acceleration constant
#define M 0.0289644 //Molar mass of the earth's air



double BarometricSensor::getAltitude(double pressure, double temp) {
    //Uses the Barometric Formula to approximate altitude above sea level, in metres. Requires pressure and temperature as arguments.

    //The variables lb, tb, pb and hb change depending on the altitude, which is approximated through temperature. These values are set in accordance to this table: https://www.avs.org/AVS/files/c7/c7edaedb-95b2-438f-adfb-36de54f87b9e.pdf
    double lb, tb, pb, hb;
    if (temp > 0) {  //when temp is greater 0 celcius, the balloon should be fairly close to the Earth's surface
        lb = -0.0065;
        tb = 288.15;
        pb = 101325;
        hb = 0;
    } else if (temp > -10)  { //when the temp is between this range, the balloon should be at least 11,000m above sea level
        lb = 0;
        hb = 1;
        tb = 216.65;
        pb = 22632.10;
    } else if (temp > -30) { //when the temp is between this range, the baloon should be at least 20,000m above sea level
        lb = 0.001;
        tb = 216.65;
        hb = 2;
        pb = 5474.89;
    } else { //when the temp is below minus 40 celcius, the balloon should be at least 32,000m above sea level
        lb = 0.0028;
        tb = 288.65;
        hb = 3;
        pb = 868.02;
    }
    //end setting of variables

    float power =  (g * M)/(R * lb); //the exponent
    if (lb != 0) {
        float pressure = pressure*100; //turn hectopascals into pascals
        pressure = pressure/pb;
        float result = pow(pressure, (1/power)); //if  power was n, this finds the nth root of pressure
        result = tb/result;
        result = result-tb;
        result = result/lb;
        result = result + hb;
        return result;
    }
    else { //when lb == 0 is a special case where a modified version of the formula must be applied. This will occur approximately 11,000m in the air
        pressure = pressure*100;
        pressure = pressure/22632.10;
        double result = log (pressure);
        result = result*1801.297428;
        result = result-0.284;
        result = result/-0.284;
        return result;
    }
}

BarometricSensor Barometric;
