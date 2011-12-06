import pygame
from pygame import locals

pygame.init()

pygame.joystick.init() # main joystick device system

try:
 j = pygame.joystick.Joystick(0) # create a joystick instance
 j.init() # init instance
 print 'Enabled joystick: ' + j.get_name()
except pygame.error:
 print 'no joystick found.'
 print pygame.joystick.get_init()

while 1:
  for e in pygame.event.get(): # iterate over event stack
    print 'event : ' + str(e.type)
    if e.type == pygame.locals.JOYBALLMOTION: # 8
      print 'ball motion' 
    elif e.type == pygame.locals.JOYHATMOTION: # 9
      print 'hat motion'
    elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
      print 'button down'
    elif e.type == pygame.locals.JOYBUTTONUP: # 11
      print 'button up'
