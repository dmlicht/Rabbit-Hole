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


while 1:
 for e in pygame.event.get(): # iterate over event stack
  #print 'event : ' + str(e.type)
  #print j.get_button(14)
  """
  if e.type == pygame.locals.JOYAXISMOTION: # 7
   x , y = j.get_axis(0), j.get_axis(1)
   print 'x and y : ' + str(x) +' , '+ str(y)
  if e.type == pygame.locals.JOYBALLMOTION: # 8
   print 'ball motion' 
  if e.type == pygame.locals.JOYHATMOTION: # 9
   print 'hat motion'
  """
  if e.type == pygame.locals.JOYBUTTONDOWN: # 10
   print 'button down'
   print e.button
  if e.type == pygame.locals.JOYBUTTONUP: # 11
   print 'button up'
