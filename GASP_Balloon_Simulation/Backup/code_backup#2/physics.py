###### Physics Stuff ####

import math
import matplotlib .pyplot as plt
import numpy as np
import time

class Physics:
    def __init__(self):
        self.g = 9.81           # gravity (m/s/s)
        self.cd = 1.47          # co-effiecent of drag
        self.rho = 1.225        # air density (kg/m^3)
        self.f = 0.0            # force (N)
        self.m = 0.5            # mass (kg)
        self.a = 0.0            # acceleration (m/s/s)
        self.v = 0.0            # velocity (m/s)
        self.A = 1.0           # area (m^2)
        self.w = 0.0            # weight (N)
        self.glid_angle = 5.0   # glid angle (degrees)
        self.temp = 15.0        # temperature (Celcius)

        self.v_vertical = 0.0

        self.prev_alt = 0.0
        self.prev_time = 0.0
   
    def gravity(self):
        """ calculate the weight force of the object """
        
        self.w = self.m * self.g
        return self.w  
    
    def velocity(self, altitude):
        """ calculate the terminal velocity of the object """
        
        w = self.gravity()
        self.air_density(altitude)
        x = self.cd * self.rho * self.A
        
        self.v = math.sqrt(((2*w)/(x))) # terminal velocity
        
        return self.v 
    
    def drag(self, alt):
        """ calculate the drag of the drag force of the object """

        self.air_density(alt)
        self.velocity(alt)

        F_drag = self.cd * self.rho * self.A * (((self.v)**2)/2)
        
        return 
    
    def air_density(self, z):
        """ calcuate the air density given the altitude of the object """
        altitude = z * 3.2808 # convert to feet
        P = self.pressure(altitude) * 100
        T = self.temperature(altitude)
        self.rho = (P / (287.05 * (T + 273.15)))

        return self.rho
    
    def pressure(self, z):
        """ Z in m, altitude in ft. Pressure in hPa """
        P = 1013 * (1-(6.87535*10**-6)*z)**5.2561
        return P
    
    def temperature(self, z):
        T = self.temp - ( 2 * (z/1000))
        return T

    def glide_angle(self, alt):
        now = time.time()
        t = self.prev_time - now
        
        if (self.prev_alt - alt) == 1:
            self.v_vertical = self.velocity(alt)
            #recalculate
            self.v = self.v_vertical / math.tan(self.glide_angle)
            
        self.prev_alt = alt
        self.prev_time = now
        
        return self.v, self.v_vertical 
    
    


