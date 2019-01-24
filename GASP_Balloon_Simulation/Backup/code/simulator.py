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
#from xml.etree import ElementTree # use for Google Maps

def update():
    ''' update everything for pygame'''
    all_sprites.draw(screen)
    pause_button_group.draw(screen)
    
    Gui.Variables(balloon.x, balloon.y, balloon.z,
                 theta, yaw,
                 wind_speed, wind_direction)

    
    pygame.display.flip()
    pygame.display.update() # Update the screen to show all changes that have been made
    screen.fill((255,255,255)) # fill the spare space where sprites are not located
    clock.tick(60)

class Balloon(pygame.sprite.Sprite):
    """ This class represents the Balloon """

    def __init__(self, altitude, x, y, home_x, home_y):
      super(Balloon, self).__init__()
      # balloon image
      self.original_img = pygame.image.load("images/arrow.png")
      self.image = self.original_img
      self.rect = self.original_img.get_rect()
      self.x, self.y = x, y
      self.home_x, self.home_y = home_x, home_y
      self.yaw = 0

      self.z = altitude # in meters 
      self.Vx, self.Vy = 1.0, 1.0
      
    def update(self):
      # update balloon location
      self.rect.x, self.rect.y = convert_coords(self.x, self.y, "pygame")    
            
    def move(self, wind_speed, wind_angle):
        
        # glide ratio 3:1
        speed = 0.5 #3*(phy.velocity(self.z))/100 ############################### approx. how manmyt iterations per second

        #print(speed)
        # convert. in other words slow the craft down
        #print("move_angle", angle)
        wind_x = math.cos(wind_angle) * ((wind_speed)/100)
        wind_y = math.sin(wind_angle) * ((wind_speed)/100)

        # calculate the x and y components
        self.Vx = math.cos(self.yaw) * speed + wind_x
        self.Vy = math.sin(self.yaw) * speed + wind_y

        """" mag = math.sqrt(self.Vx**2 + self.Vy**2)
        if mag > 5:
            self.Vx /= mag
            self.Vy /= mag
            self.Vx *= 5
            self.Vy *= 5"""
    
        #time = time + time_step
        self.x += self.Vx #* time_step
        self.y += self.Vy  #* time_step
        print(self.Vx, self.Vy)
        
        self.image = pygame.transform.rotate(self.original_img, self.yaw) # reversed angular rotation 

    def compute_theta(self):
        """ calculate theta in relation to home """

        d_x = self.x - self.home_x #- self.x
        d_y = self.y - self.home_y #- self.y

        print(d_x,d_y)
    
        c = math.sqrt(((d_x ** 2) + (d_y ** 2))) #distance from home
        #print(c)
        theta = math.atan2(d_y,d_x)
        theta = math.degrees(theta)
        #print("theta", theta)

        return theta
            
class Home(pygame.sprite.Sprite):
    """ This class represents the Home base (landing location)"""
    def __init__(self, lat, lon):
        super(Home, self).__init__()
        self.image = pygame.image.load("images/home.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = convert_coords(lat, lon, "pygame")

       
def computePID(setpoint,
             _input, last_error, prev_time,
               error_sum):
    """ PID algorithm for anything """
    kp = 1
    kd = 0
    ki = 0

    current_time = time.time()
    d_time = current_time - prev_time
    
    error = setpoint - _input
    #print("error", error)

    #print 'angle:', setpoint,_input

    error_sum = (error * d_time)
    
    d_error = (last_error - error) / d_time

    output = kp * error + kd * d_error + ki * error_sum 
    last_error = error
    prev_time = current_time
    # PID has not been changed to fit the needs required 
    print("output", output)
    return output, last_error, prev_time, error_sum


def comput_angle(x, y):
    """ calculate the yaw of the object"""
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
    variables = {}
    # open file
    for line in open("config.txt"):
        # read file
        var, value = line.split(',')
        try:
            variables[var] = float(value)
        except ValueError:
            variables[var] = value
        
    
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
 longitude, latitude, altitude) = config()

screen = pygame.display.set_mode((width, height))
screen_rect = pygame.Rect((0,0),(width, height))
clock = pygame.time.Clock()

Gui = gui.GUI(screen, width, height) 

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
yaw = 0
dummy_variable = 0

# algorithm variables
error_sum, last_error, prev_time = 0, 0, 0
output_lon, output_lat = 0, 0 


# sprites
all_sprites = pygame.sprite.Group()

balloon = Balloon(altitude,latitude,longitude,home_lat,home_lon)
home = Home(home_lat,home_lon)

all_sprites.add(balloon)
all_sprites.add(home)
theta = balloon.compute_theta()

phy = physics.Physics(cd, mass, area, temp, glide_angle)
# Serial port - from Arduino
"""while not ser:
    try:
        ser = serial.Serial(port, 9600) # name/path needs to be changed
    except:
        print("Not connected")"""

#Gui.TitleScreen() # Display the title screen
#pygame.time.delay(2000) # wait 2 seconds then change screens

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
            ser = serial.Serial(port, 9600) # name/path needs to be changed
        except:
            pass
            
    print(ser.readline()) # read from serial port """

    # interpret data
    
    #output_lon, output_lat, last_error_lat ,last_error_lon, prev_time = xyzPID(home_lon, home_lat, home_alt,
    #                                                                longitude, latitude, altitude, error_Sum, last_error_lon, last_error_lat, prev_time)

    ## Pause data stream
    while finish == 'pause':
        finish = Gui.Pause(balloon.x, balloon.y, balloon.z,
                 theta, yaw,
                 wind_speed, wind_direction,
                 all_sprites, pause_button)
        
    while finish == 'landed':
        finish = Gui.Landed(balloon.x, balloon.y, balloon.z,
                 theta, yaw,
                 wind_speed, wind_direction,
                 all_sprites, pause_button)
        
    if finish == "restart":
        print("Restarted")
        
        all_sprites.empty()
        (width, height, port,
         cd, mass, area, temp, glide_angle,
         wind_speed, wind_direction,
         home_lon, home_lat, home_alt,
         longitude, latitude, altitude) = config()
        
        theta = 0
        yaw = 0

        # algorithm variables
        error_Sum, last_error, prev_time = 0, 0, 0
        output_lon, output_lat = 0, 0 

        balloon = Balloon(altitude,latitude,longitude,home_lat,home_lon)
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
        balloon.yaw += output
        
        balloon.move(wind_speed, wind_direction)
        balloon.z -= phy.velocity(balloon.z) / 100 # move the balloon in the Z axis (falling). Dividced by iterations per second 
    balloon.update()
    
    # Keyboard Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
          finish = "quit"

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE: # pause using keyboard 
          finish = "pause"

        if event.type == pygame.MOUSEBUTTONUP:  # check if button clicked
          pos = pygame.mouse.get_pos()
          if pause_button.rect.collidepoint(pos): # pause using mouse click 
            finish = "pause"
        if event.type == pygame.KEYDOWN and event.key == K_r: # restartr the simulation 
            finish = "restart"

    update() # update screen
    
pygame.quit()



######
## NOTES
######

# theta not changing dutringf flight
# bearing = 90 - theta
