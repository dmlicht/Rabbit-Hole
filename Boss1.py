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

## end of import

#rabbyt.set_viewport((800,600))

class Boss(rabbyt.Sprite):
   def __init__(self, screen):
      rabbyt.Sprite.__init__(self, '1DragonBoss.png', (-144, 144, 144, -144))

      self.health = 30
      self.dir = random.randint(0,7)
      self.speed = 4
      self.pause = 20

      self.offset = 144

      self.xy = (0,0)

      self.dx_values = (1,  .7,  0, -.7, -1, -.7, 0, .7)
      self.dy_values = (0,  -.7,  1, -.7,  0,  .7, 1, .7)

      self.dx = self.dx_values[self.dir] * self.speed
      self.dy = self.dy_values[self.dir] * self.speed

      self.bounding_radius = 100

      self.screen = screen

   def update(self):
       if self.pause == 0:
          self.pause = 20
          self.calculate_direction()
       else:
          self.pause -= 1

       self.x += self.dx
       self.y += self.dy
       if self.check_vertical_bounds() or self.check_horizontal_bounds():
          self.pause = 0
            
   def calculate_direction(self):
       randomint = random.randint(0,1)
       if randomint == 0:
          self.turn_left()
       if randomint == 1:
          self.turn_right()
       self.dx = self.dx_values[self.dir] 
       self.dy = self.dy_values[self.dir] 
        
       self.dx *= self.speed
       self.dy *= self.speed

   def hone_in(self, p_x, p_y):
       bit_x = p_x-self.x
       bit_y = p_y-self.y
       self.dx = bit_x/math.sqrt(bit_x*bit_x + bit_y*bit_y)
       self.dy = bit_y/math.sqrt(bit_x*bit_x + bit_y*bit_y)
       self.x += self.dx*self.speed
       self.y += self.dy*self.speed
          
   def turn_left(self):
        #self.dir += random.randint(0,90)
        self.dir += 1
        if self.dir > 7:
            self.dir = 0

   def turn_right(self):
        #self.dir -= random.randint(0,90)
        self.dir -= 1
        if self.dir < 0:
            self.dir = 7

   def check_horizontal_bounds(self): 
        if self.x > self.screen.get_width()/2 - self.offset:
            self.x = self.screen.get_width()/2 - self.offset
            return True
        if self.x < -self.screen.get_width()/2 + self.offset:
            self.x = -self.screen.get_width()/2 + self.offset
            return True
        return False

   def check_vertical_bounds(self): 
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
        return 0

   def lose_health(self, dmg):
       self.health -= dmg
       return self.health <= 0

