#ifndef GPS_Sensor
#define GPS_Sensor

#include "Sensor.h"
#include "TinyGPSPlusPlus.h"

class GPSSensor : public Sensor {
public:

    boolean setup(void);
    void headers(File* f);
    void write(File* f);
    void encodeSerial();
    void print_data();
    

    TinyGPSPlus gps;
    double getLng();
    double getLat();
    double getTime();
    double getAlt();
};

extern GPSSensor GPS;

#endif
