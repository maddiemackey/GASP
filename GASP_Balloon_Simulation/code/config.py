# Configuration File for the G(A)SP Simulator
# Almost all variables should be provided in float form, unless otherwise stated. 

# Pygame Screen Variables (Should be integers, otherwise they will be rounded) 
width = 800
height = 600

# The Port used to communicate with an external microcontroller (Arduino). MUST be a string.
port = 'COM3'

# Physics Variables
# cd = Co-efficent of Drag (dependent on the shape of the parachute (currently assumed to be circular)). 
# area = area of the parachute
# angle = the angle the object faces to start with. (North=90, East=0, South=180, West=270)
# temp = temperature at surface
# glide_angle = tilt of the object while desccending
cd = 1.47
mass = 1    # kilograms
area = 1    # m^2
temp = 15.0 # Celcius
glide_angle = 5.0 # degrees

# Wind Variables 
wind_scale = 0    
wind_direction = -90

# Location Variables 
home_lon = 0
home_lat = 0
home_alt = 0

# Object Location Variables. (Where the balloon will start)
longitude = 100
latitude = 100
altitude = 30000

