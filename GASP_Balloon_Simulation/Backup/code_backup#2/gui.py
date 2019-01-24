#### GUI Screens #####

import pygame
from pygame.locals import *

class GUI:

  def __init__(self, screen, width, height):

    self.screen = screen
    self.height = height
    self.width = width

  def TitleScreen(self):
    ''' display the title screen '''
    
    title = pygame.font.SysFont("Arial", 50)
    subtitle = pygame.font.SysFont("Arial", 30)
    string_list = "G(A)SP Simulator"
    pre_string = []
    
    for i in string_list:
        self.screen.fill((0,0,0))
        pre_string.append(i)
        string = ''.join(pre_string)
        _title = title.render(str(string), True, (255,255,255))
        title_rect = _title.get_rect(centerx=self.width/2+110, centery=200)
        self.screen.blit(_title, title_rect)

        logo = pygame.sprite.Sprite()
        images = pygame.sprite.Group()
        logo.image = pygame.image.load("images/logo.png")
        logo.rect = logo.image.get_rect()
        logo.rect.x, logo.rect.y = 75, (self.height/2)-154

        images.add(logo)
        
        images.draw(self.screen)
    
        pygame.display.update()
        pygame.time.delay(50)
        
    string_list = "Andrew Wilkie     Maddie Mackey"
    pre_string = []

    for i in string_list:
      self.screen.fill((0,0,0))
      pre_string.append(i)
      string = ''.join(pre_string)
      _author = subtitle.render(str(string), True, (192,192,192))
      author_rect = _author.get_rect(centerx=self.width/2+110, centery=350)
      self.screen.blit(_author, author_rect)
      self.screen.blit(_title, title_rect)

      logo = pygame.sprite.Sprite()
      images = pygame.sprite.Group()
      logo.image = pygame.image.load("images/logo.png")
      logo.rect = logo.image.get_rect()
      logo.rect.x, logo.rect.y = 75, (self.height/2)-154

      images.add(logo)
      
      images.draw(self.screen)

      pygame.display.update()
      pygame.time.delay(50)

    self.screen.blit(_title, title_rect)
    self.screen.blit(_author, author_rect)

    pygame.display.update()

  def Disconnected(self, label):
    """ object disconnected from serial """

    font = pygame.font.SysFont("Arial", 15)
    
    pygame.time.set_timer(pygame.USEREVENT, 500) # set the timer for the flashing message

    dis_con = font.render("DISCONNECTED", True, (0,0,0))
    self.screen.blit(dis_con, (self.width/2, 0))

    for event in pygame.event.get():
      # flashing continue message
      if event.type == pygame.USEREVENT and label: # 'flash' the text, switch it from white to grey
          dis_con = font.render("DISCONNECTED", True, (0,0,0))
          label = False
        
      elif event.type == pygame.USEREVENT and label == False:
        dis_con = font.render("DISCONNECTED", True, (255,255,255))
        label = True


      if event.type == pygame.QUIT:
          return "quit"

      if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
          return "quit"

   
    return None

  def Variables(self, x_in, y_in, z_in, theta, direction):
    """ display the location of the object """
    altitude = round(z_in/float(1000), 2)
    
    font = pygame.font.SysFont("Arial", 15)
    sprites = pygame.sprite.Group()
    altitude_group = pygame.sprite.Group()
    
    direction_sprite = pygame.sprite.Sprite()
    theta_sprite = pygame.sprite.Sprite()
    altitude_indicator = pygame.sprite.Sprite()
    altitude_level = pygame.sprite.Sprite()

    direction_sprite.image = pygame.image.load("images/indicator.png")
    theta_sprite.image = pygame.image.load("images/indicator.png")
    altitude_level.image = pygame.image.load("images/altitude.png")
    altitude_indicator.image = pygame.image.load("images/altitude_indicator.png")
    
    
    direction_sprite.rect = direction_sprite.image.get_rect(x=self.width-80, y=60)
    theta_sprite.rect = theta_sprite.image.get_rect(x=self.width-80, y=0)
    altitude_level.rect = altitude_indicator.image.get_rect(x=self.width-70, y=125)
    altitude_indicator.rect = altitude_indicator.image.get_rect(x=self.width-67, y=175-(altitude))
    
    sprites.add(direction_sprite, theta_sprite, altitude_level)
    altitude_group.add(altitude_indicator)

    direction_sprite.image = pygame.transform.rotate(direction_sprite.image, direction)
    theta_sprite.image = pygame.transform.rotate(theta_sprite.image, theta)

    
    x = font.render("X  "+str(int(x_in)) , True, (0,0,0))
    y = font.render("Y  "+str(int(y_in)), True, (0,0,0))
    z = font.render("Z  "+str(int(z_in)), True, (0,0,0))

    theta = font.render("Theta  "+str(int(theta))+u"\u00b0", True, (0,0,0))
    direction = font.render("Yaw(F/ E) "+str(int(direction))+u"\u00b0", True, (0,0,0))
    altitude = font.render("Altitude  "+str(altitude)+"km", True, (0,0,0))
    
    self.screen.blit(x, ((self.width/3)/2, self.height-20))
    self.screen.blit(y, (((self.width/3)*3)/2 ,self.height-20))
    self.screen.blit(z, (((self.width/3)*5)/2 ,self.height-20))

    self.screen.blit(theta, ((self.width-100), 40))
    self.screen.blit(direction, ((self.width-100), 100))
    self.screen.blit(altitude, ((self.width-100), 190))

    sprites.draw(self.screen)
    altitude_group.draw(self.screen)
    
    #pygame.display.update()
    #clock.tick(60)

  def Pause(self, x_in, y_in, z_in, theta, direction, sprites, pause_button):

    self.screen.fill((255,255,255))
    pause_button_group = pygame.sprite.GroupSingle(pause_button)
    
    self.Variables(x_in, y_in, z_in, theta, direction)

    finish = 'pause'
    
    font = pygame.font.SysFont("Arial", 15)

    
    pause_title = font.render("PAUSED", True, (0,0,0))

    self.screen.blit(pause_title, (self.width/2, 0))
    sprites.draw(self.screen)
    pause_button_group.draw(self.screen)
    
    
    self.screen.set_alpha(255)
    for event in pygame.event.get():

      if event.type == pygame.QUIT:
          return "quit"

      if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
          return ""

      if event.type == pygame.MOUSEBUTTONUP:  # check if button clicked
        pos = pygame.mouse.get_pos()
        if pause_button.rect.collidepoint(pos): # pause
          return ""
        
    pygame.display.update()


    return finish
    

    

pygame.init()
clock = pygame.time.Clock()
