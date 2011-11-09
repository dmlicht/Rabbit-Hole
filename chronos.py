## beginning of import
from __future__ import division
import pygame, rabbyt, sys

from math import cos, sin, radians
import random
import os.path

import settings

#rabbyt.data_directory = os.path.dirname(__file__)
#rabbyt.set_default_attribs()

## end of import

#rabbyt.set_viewport((800,600))

class Spark(rabbyt.Sprite):

   def __init__(self, screen, xy):
      rabbyt.Sprite.__init__(self, '1energy.png')

      self.speed = -3
      self.xy = xy
      self.rot = 0

      self.time_last = pygame.time.get_ticks() 
      self.screen = screen

   def update(self):
       self.y += self.speed
       self.rot += 0.4

   def checkBounds(self):
       if self.x >= 350 or self.y >= 450 or self.x <= -350 or self.y <= -450:
           return True
       return False
