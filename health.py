from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random
import settings
from settings import Font, FontSprite

SCREEN_SIZE = (800,600)
STARTING_SCREEN = "Menu Screen"

screen = pygame.display.set_mode(SCREEN_SIZE, pygame.OPENGLBLIT | pygame.DOUBLEBUF)
rabbyt.set_viewport(SCREEN_SIZE)
rabbyt.set_default_attribs()

bar = rabbyt.Sprite(0, (0,20,200,0))
char = rabbyt.Sprite("1grasstile.png", (-50,50,50,-50))
bar.rgb = (34,139,34)
bar.xy = (0,0)


while True:
   rabbyt.clear()
   bar.render()
   char.render()
   rabbyt.set_time(pygame.time.get_ticks()/1000.0)

   pressed = pygame.key.get_pressed()

   char.y += 7*(pressed[K_UP] - pressed[K_DOWN])
   char.x += 7*(pressed[K_RIGHT] - pressed[K_LEFT])

   clicked = pygame.mouse.get_pressed()[0]
   if clicked and bar.shape[2][0] > 0:
      temp = bar.shape
      print temp
      bar.shape = (0,temp[1][1],temp[2][0]-10,0)

   for event in pygame.event.get():
       if event.type ==  QUIT:
           sys.exit()
   pygame.display.flip()