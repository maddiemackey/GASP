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
                 theta, yaw)

    
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

      self.z = altitude # in meters 
      self.Vx, self.Vy = 1.0, 1.0  
      
    def update(self):
      # update balloon location
      self.rect.x, self.rect.y = convert_coords(self.x, self.y, "pygame")    
            
    def move(self, angle):
        
        speed = 0.5 #phy.velocity(self.z) / 3.6
        # convert to km/h. in other words slow the craft down
        #print("angle_move", angle)
        # sine and cos need to change when quadrants change... possibly
        # move does not move object in the same dircetion as planned
        
        self.Vx = math.cos(angle) * speed # + wind
        self.Vy = math.sin(angle) * speed # + wind
        self.x += self.Vx
        self.y += self.Vy
        
        self.image = pygame.transform.rotate(self.original_img, angle) # reversed angular rotation 
        #print("ang", angle)
        
        #print("x", self.x)
        #print("Y", self.y)
        
    def compute_theta(self):


        d_x = self.x - self.home_x
        d_y = self.y - self.home_y

        #print(d_x,d_y)
    
        c = math.sqrt(((d_x ** 2) + (d_y ** 2))) #distance from home
        #print(c)
        theta = math.atan2(d_x,d_y)
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
             _input, last_error, prev_time):
    """ PID algorithm for anything """
    kp = 0.5
    kd = 5
    ki = 0.02

    current_time = time.time()
    d_time = current_time - prev_time
    
    error = setpoint - _input
    #print("error", error)

    #error_sum += (error * d_time)
    
    d_error = (error - last_error) / d_time

    output = kp * error #+ kd * d_error#ki * error_sum + kd * d_error
    last_error = error
    prev_time = current_time
    
    return output, last_error, prev_time


def xyzPID(home_lon, home_lat, home_alt,
           lon, lat, alt,
           error_sum, last_error_lon, last_error_lat, prev_time):
    """ calculates PID for x, y and z """
    #x PID
    output_lon, last_error_lon, prev_time = calculatePID(home_lon,lon,error_sum, last_error_lon, prev_time)
    #y PID
    output_lat, last_error_lat, prev_time = calculatePID(home_lat,lat,error_sum, last_error_lat, prev_time)
    #z PID
    #calculatePID(home_alt,
    #             alt,
    #             error_sum, last_error_alt, prev_time)
    
    return output_lon, output_lat, last_error_lat, last_error_lon, prev_time

def computeYaw(Vx, Vy):
    """ calculate the yaw of the object"""
    #print(Vx, Vy)
    if Vx > 0:
        if Vy > 0:
            angle = (math.degrees(math.atan2(Vy,Vx)))#+ how far it is from the x axis)
            #print(angle)
            return angle 
        elif Vy < 0:
            angle = (math.degrees(math.atan2(Vy,Vx)) )#- how far from x axis)
            #print(angle)
            return angle
    else:
        #print(math.degrees(math.atan2(Vy,Vx)))
        return math.degrees(math.atan2(Vy,Vx))
    

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



# pygame setup
pygame.init()

width = 800
height = 600
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
port = 'COM3' # name of the port 

# physics variables
mass = None
area = None
angle = 0 
speed = 1   # speed of object 
force = None

# Object variables
home_lon, home_lat, home_alt = 0, 0, 0 # longitude = Y, latitude = X
longitude, latitude, altitude = 300, -400, 43000 # cartesian plane coordinates 
#bearing = 0 # compass bearing
theta = 0
yaw = 0

# algorithm variables
error_Sum, last_error, prev_time = 0, 0, 0
output_lon, output_lat = 0, 0 


# sprites
all_sprites = pygame.sprite.Group()

balloon = Balloon(altitude,latitude,longitude,home_lat,home_lon)
home = Home(home_lat,home_lon)

all_sprites.add(balloon)
all_sprites.add(home)
theta = balloon.compute_theta()

phy = physics.Physics()
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
                 all_sprites, pause_button)
    
    theta = balloon.compute_theta() 
    yaw = computeYaw(balloon.x, balloon.y)
    output, last_error, prev_time = computePID(theta+180, yaw, last_error, prev_time)

    if balloon.z > home_alt: 
        balloon.move(yaw+180)
    #bearing = 90 - theta
    yaw += output
    #balloon.move(yaw)
    balloon.z -= phy.velocity(balloon.z) # move the balloon in the Z axis (falling)
    if balloon.z <= home_alt:
        balloon.z = home_alt
    
    balloon.update()
    
    # Keyboard Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
          finish = "quit"

        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
          finish = "pause"

        if event.type == pygame.MOUSEBUTTONUP:  # check if button clicked
          pos = pygame.mouse.get_pos()
          if pause_button.rect.collidepoint(pos): # pause
            finish = "pause"
          

    update() # update screen 
    
pygame.quit()




## buttons, pause 
# theta not changing dutringf flight
# everything in cartesian (excpet display )
