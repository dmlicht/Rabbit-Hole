## beginning of import
from __future__ import division
import pygame, rabbyt, sys

import math
from math import cos, sin, radians
import random
import os.path

import settings

#rabbyt.data_directory = os.path.dirname(__file__)
#rabbyt.set_default_attribs()

#rabbyt.set_viewport((800,600))

class Boss_zero(rabbyt.Sprite):
   def __init__(self, screen):
      rabbyt.Sprite.__init__(self, '1DragonBoss.png', (-144, 144, 144, -144))

      self.health = 20
      self.speed = 4
      self.offset = 144
      self.left = True
      self.xy = (-50,100)

      self.bounding_radius = 100

      self.screen = screen
      self.x = rabbyt.chain(
                    rabbyt.lerp(0, -300, dt=2),
                    rabbyt.lerp(-300, 300, dt=4, extend="reverse"))

   """
   def update(self):
       if self.left:
           self.x -= self.speed
       else:
           self.x += self.speed
   """
           
   def attack(self):
        if self.y >= -100:
            self.y -= 10

   def retreat(self):
        if self.y <= 300:
            self.y += 10         

   def check_horizontal_bounds(self): 
        if self.x > (self.screen.get_width()/2): #- self.offset:
            #self.x = (self.screen.get_width()/2) - self.offset
            self.left = True
            print 'first if'
            
        elif (self.attrgetter('x') < -self.screen.get_width()/2): #+ self.offset:
            #(self.x = self.screen.get_width()/2) + self.offset
            self.left = False
            print 'second if'

   """def check_vertical_bounds(self): 
        if self.y > 300 - self.offset - 15:
            self.y = 300 - self.offset - 15
            return True
        if self.y < -self.screen.get_height()/2 + self.offset + 150:
            self.y = -self.screen.get_height()/2 + self.offset + 150
            return True
        return False

   def attack_pattern(self):
        at_pat = random.randint(0,10)
        if at_pat >=0 and at_pat <=6:
           return 0
        elif at_pat >= 7 and at_pat <= 9:
           return 1
        elif at_pat == 10:
           return 2
        return 0"""

   def lose_health(self, dmg):
       self.health -= dmg
       return self.health <= 0
