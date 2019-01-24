#### Pygame Simulator ####

##########################
##  Simulator 
##  IT 2016
##
## Andrew Wilkie, Maddie Mackey
##########################

# Imported modules
import pygame
from pygame.locals import *
import math, random
import sys#, serial
import gui, physics
import time
#import googlemaps # used for Google Maps 

def update():
    ''' update everything for pygame'''
    all_sprites.draw(screen)
    pause_button_group.draw(screen)
    
    Gui.Variables(balloon.x, balloon.y, balloon.z,
                 theta, balloon.yaw,
                 wind_speed, wind_direction) # Send data to the GUI file to update the variables and meters on screen.

    
    pygame.display.flip()
    pygame.display.update() # Update the screen to show all changes that have been made
    screen.fill((255,255,255)) # fill the spare space where sprites are not located
    clock.tick(60)

class Balloon(pygame.sprite.Sprite):
    """ This class represents the Balloon """

    def __init__(self, altitude, x, y, home_x, home_y, yaw):
      super(Balloon, self).__init__()
      # balloon image
      self.original_img = pygame.image.load("images/arrow.png")
      self.image = self.original_img
      self.rect = self.original_img.get_rect()
      self.x, self.y = x, y
      self.home_x, self.home_y = home_x, home_y
      self.yaw = yaw

      self.z = altitude # altitude of the balloon (in meteres) 
      self.Vx, self.Vy = 1.0, 1.0
      
    def update(self):
      # update balloon location
      self.rect.center = convert_coords(self.x, self.y, "pygame")    
            
    def move(self, wind_speed, wind_angle):
        
        # glide ratio 3:1
        speed = 0.5 #3*(phy.velocity(self.z))#/100 # divided by approximately how many iterations per second. Used to slow the craft down and be more realistic.

        # Calculate the X and Y components of the Wind using the Wind speed and direction
        wind_x = math.cos(wind_angle/57.2958) * ((wind_speed)/100)
        wind_y = math.sin(wind_angle/57.2958) * ((wind_speed)/100)

        # calculate the x and y components of the balloon 
        #maths cos and sin work in radians. Convert back into degrees by dividing by radian number
        self.Vx = math.cos(self.yaw/57.2958) * speed + wind_x
        self.Vy = math.sin(self.yaw/57.2958) * speed + wind_y
    
        #time = time + time_step
        self.x += self.Vx #* time_step
        self.y += self.Vy  #* time_step
        
        self.image = pygame.transform.rotate(self.original_img, self.yaw) # reversed angular rotation 

    def compute_theta(self):
        """ calculate theta in relation to home """

        d_x = self.x - self.home_x # get the difference between the balloon's location and home's location.
        d_y = self.y - self.home_y 
    
        c = math.sqrt(((d_x ** 2) + (d_y ** 2))) # distance from home

        theta = math.atan2(d_y,d_x) # calculate the angle (in Radians)
        theta = math.degrees(theta) # convert the angle from radians to degrees 

        return theta
            
class Home(pygame.sprite.Sprite):
    """ This class represents the Home base (landing location)"""
    def __init__(self, lat, lon):
        super(Home, self).__init__()
        self.image = pygame.image.load("images/home.png")
        self.rect = self.image.get_rect()
        self.rect.center = convert_coords(lat, lon, "pygame")

       
def computePID(setpoint,
             _input, last_error, prev_time,
               error_sum):
    """ PID algorithm """
    # PID constants
    kp = 1
    kd = 0
    ki = 0

    current_time = time.time()
    d_time = current_time - prev_time
    
    error = setpoint - _input

    error_sum = (error * d_time)
    
    d_error = (last_error - error) / d_time

    output = kp * error + kd * d_error + ki * error_sum 
    last_error = error
    prev_time = current_time
    # PID has not been changed to fit the needs required 

    return output, last_error, prev_time, error_sum


def comput_angle(x, y):
    """ calculate any angle """
    return math.degrees(math.atan2(y, x))
    

def convert_coords(x, y, conversion):
    """Convert coordinates into pygame coordinates."""    
    if conversion == "cartesian" :
        # convert to cartesian plane coordinates 
        x_new = x - (width/2)
        y_new = (height/2) + y 

    elif conversion == "pygame":
        # only needed to place images in pygame
        x_new = x + (width/2)
        y_new = (height/2)  - y
        
    return x_new, y_new

def config():
    """ read config file and assign variables """
    variables = {} # variable dictionary. created when the file is read.
    # open file
    for line in open("config.txt"):
        # read file
        if not line.startswith('#') and not line.startswith("\n"): # check to see if the line is a comment of blank
            var, value,  = line.split(',')
            try:
                variables[var] = float(value) # add to the variables dictionary
            except ValueError:
                variables[var] = value # port name will be assigned using this one 
            
        
    
    # assign variables
    width, height = int(variables['width']), int(variables['height']) # pygame screen 
    port = variables['port'] # name of the port 

    # physics variables
    cd = variables['cd'] 
    mass = variables['mass']
    area = variables['area']
    temp = variables['temp']
    glide_angle = variables['glide_angle']

    wind_speed = variables['wind speed']
    wind_direction = variables['wind direction']

    # Object variables
    home_lon, home_lat, home_alt = variables['home lon'], variables['home lat'], variables['home alt'] # longitude = Y, latitude = X
    longitude, latitude, altitude = random.randint(-500,500), random.randint(-500,500), random.randint(0,43000) #For testing purposes  
    #longitude, latitude, altitude = variables['longitude'], variables['latitude'], variables['altitude']
    return (width, height, port,
            cd, mass, area, temp, glide_angle,
            wind_speed, wind_direction,
            home_lon, home_lat, home_alt,
            longitude, latitude, altitude)
        

# pygame setup
pygame.init()

(width, height, port,
 cd, mass, area, temp, glide_angle,
 wind_speed, wind_direction,
 home_lon, home_lat, home_alt,
 longitude, latitude, altitude) = config() # assign all the variables before beginning the simulation 

screen = pygame.display.set_mode((width, height)) # build the screen 
screen_rect = pygame.Rect((0,0),(width, height))
clock = pygame.time.Clock()

Gui = gui.GUI(screen, width, height) # initiate the GUI file 

pygame.display.set_caption("G(A)SP Simulator") # window title

font = pygame.font.SysFont("monospace", 11)

## pause button
pause_button = pygame.sprite.Sprite()
pause_button.image = pygame.image.load('images/pause_button.png')
pause_button.rect = pause_button.image.get_rect()
pause_button_group = pygame.sprite.GroupSingle(pause_button)
pause_button.rect.top = 10
pause_button.rect.left = 10

# other variables
finish = '' # pygame loop variable
ser = False # serial port
"""port = 'COM3' # name of the port 

"""
theta = 0
#if velocity on both x and y is the same, initial yaw must then be 45
yaw = 45

# algorithm variables
error_sum, last_error, prev_time = 0, 0, 0
output_lon, output_lat = 0, 0 


# sprites
all_sprites = pygame.sprite.Group() 

balloon = Balloon(altitude,latitude,longitude,home_lat,home_lon,yaw)
home = Home(home_lat,home_lon)

all_sprites.add(balloon)
all_sprites.add(home)
theta = balloon.compute_theta()

phy = physics.Physics(cd, mass, area, temp, glide_angle) # initialise the Physics file 
# Serial port - from Arduino
"""while not ser:
    try:
        ser = serial.Serial(port, 9600) # try to connect to the serial port
    except:
        print("Not connected") # warn the user that the serial port is not connected"""

Gui.TitleScreen() # Display the title screen
pygame.time.delay(2000) # wait 2 seconds then change screens

# Main loop
while (finish != 'quit'):

    #print balloon.Vx,balloon.Vy
    # recieve data
    """while (not ser):
        # Serial disconnected
        screen.fill((255,255,255))
        finish = Gui.Disconnected()
        update()
        try:
            ser = serial.Serial(port, 9600) # assign the serial port to a variable 
        except:
            pass
            
    print(ser.readline()) # read from serial port """

    ## Pause data stream
    while finish == 'pause':
        """ pause the simulation """
        finish = Gui.Pause(balloon.x, balloon.y, balloon.z,
                 theta, balloon.yaw,
                 wind_speed, wind_direction,
                 all_sprites, pause_button)
        
    while finish == 'landed':
        """ display all the last know data and tell the user the simulation has ended """ 
        finish = Gui.Landed(balloon.x, balloon.y, balloon.z,
                 theta, balloon.yaw,
                 wind_speed, wind_direction,
                 all_sprites, pause_button)
        
    if finish == "restart":
        """ restart the simulation """
        print("Restarted")

        # Empty the sprite groups
        all_sprites.empty()

        # reassign variable
        (width, height, port,
         cd, mass, area, temp, glide_angle,
         wind_speed, wind_direction,
         home_lon, home_lat, home_alt,
         longitude, latitude, altitude) = config()

        theta = 0
        #if velocity on both x and y is the same, initial yaw must then be 45
        yaw = 45

        # algorithm variables
        error_Sum, last_error, prev_time = 0, 0, 0
        output_lon, output_lat = 0, 0 

        balloon = Balloon(altitude,latitude,longitude,home_lat,home_lon,yaw)
        home = Home(home_lat,home_lon)

        all_sprites.add(balloon)
        all_sprites.add(home)
        finish = '' # pygame loop variable


    # limit the baloons z axis. So it doesnt fall into nothingness
    if balloon.z <= home_alt:
        balloon.z = home_alt
        finish = "landed"
        #circle home if not at correct altitude
    else:
        # move baloon
        theta = balloon.compute_theta()
        
        velocity_angle = comput_angle(balloon.Vx, balloon.Vy)
            
        output, last_error, prev_time, error_sum = computePID(theta+180, velocity_angle, last_error, prev_time, error_sum)
        balloon.yaw = (balloon.yaw + output) %360 # mod 360 to limit the numbers to 360 
        
        balloon.move(wind_speed, wind_direction)
        balloon.z -= phy.velocity(balloon.z) / 100 # move the balloon in the Z axis (falling). Dividced by iterations per second 
    balloon.update()
    
    # Keyboard Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
          finish = "quit"

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE: # exit using keyboard 
          finish = "quit"

        if event.type == pygame.KEYDOWN and event.key == K_p: # pause using keyboard 
          finish = "pause"

        if event.type == pygame.MOUSEBUTTONUP:  # check if button clicked
          pos = pygame.mouse.get_pos()
          if pause_button.rect.collidepoint(pos): # pause using mouse click 
            finish = "pause"
        if event.type == pygame.KEYDOWN and event.key == K_r: # restart the simulation 
            finish = "restart"

    update() # update screen
    
pygame.quit()

##################
## NOTES
##################
# will glitch when it reaches home (0,0)
# flip the x and y in the atan2 function to get angle from north
# else the angle is from x positive 
