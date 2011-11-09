## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings

class Dragon(rabbyt.Sprite):
  def __init__(self, name, screen, at_pattern, mov_pattern, specified_x_position=False):
    rabbyt.Sprite.__init__(self, name+'.png', (-91.7857143, 74, 91.7857143, -74))
    self.screen = screen
    self.frame = 0
    self.enemy_tex = [((0.0, 0.578125), (0.0896344855427742, 0.578125), (0.0896344855427742, 0.0), (0.0, 0.0)), \
                      ((0.0896344855427742, 0.578125), (0.17926897189710855484, 0.578125), (0.17926897189710855484, 0.0), (0.0896344855427742, 0.0)), \
                      ((0.17926897189710855484, 0.578125), (0.2689034630789032, 0.578125), (0.268903463078903, 0.0), (0.17926897189710855484, 0.0)), \
                      ((0.2689034630789032, 0.578125), (0.3585379421710968, 0.578125), (0.3585379421710968, 0.0), (0.2689034630789032, 0.0)), \
                      ((0.3585379421710968, 0.578125), (0.44817242026329041, 0.578125), (0.44817242026329041, 0.0), (0.3585379421710968, 0.0)), \
                      ((0.44817242026329041, 0.578125), (0.5378069281578064, 0.578125), (0.5378069281578064, 0.0), (0.44817242026329041, 0.0)), \
                      ((0.5378069281578064, 0.578125), (0.62744140625, 0.578125), (0.62744140625, 0.0), (0.5378069281578064, 0.0))]

    self.tex_shapes = [((0.0,0.796875), (0.3177083432674408,0.796875), (0.3177083432674408,0.0), (0.0,0.0)), \
                       ((0.3177083432674408,0.796875), (0.63541668653488159,0.796875), (0.63541668653488159,0.0), (0.3177083432674408,0.0)), \
                       ((0.63541668653488159,0.796875), (0.953125,0.796875), (0.953125,0.0), (0.63541668653488159,0.0))]

    self.offset = 74

    if not specified_x_position:
      self.x = random.randint(-300,300)
    else:  self.x = specified_x_position
    self.y = 400 #random.randint(300, 400)

    self.at_pat = at_pattern
    self.mov_pat = mov_pattern
    self.speed = -3

    self.offsetx = 74
    self.offsety = -91.7857143

    self.time_last = pygame.time.get_ticks() 
    self.bounding_radius = 30

    self.past_x = self.x
    self.past_y = self.y
    if self.at_pat == 1:
      self.x = self.x
      self.y = self.y
    elif mov_pattern == 0:
      self.x = rabbyt.chain( rabbyt.lerp(self.x, self.x+50, dt=1),
                           rabbyt.lerp(self.x+50, self.x, dt=1),
                           rabbyt.lerp(self.x, self.x-50, dt=1, extend="reverse"),)
    elif mov_pattern == 1:
      self.x = rabbyt.chain( rabbyt.lerp(self.x, self.x-50, dt=1),
                           rabbyt.lerp(self.x-50, self.x, dt=1),
                           rabbyt.lerp(self.x, self.x+50, dt=1, extend="reverse"),)
    elif mov_pattern == 2:
      self.y = rabbyt.chain( rabbyt.lerp(self.y, self.y-300, dt=2),
                           rabbyt.lerp(self.y-300, self.y-150, dt=2),
                           rabbyt.lerp(self.y-150, self.y-450, dt=2),
                           rabbyt.lerp(self.y-450, self.y-400, dt=2),
                           rabbyt.lerp(self.y-400, self.y-1000, dt=2, extend="reverse"),)
      self.x = rabbyt.chain( rabbyt.lerp(self.x, self.x+50, dt=3/2),
                           rabbyt.lerp(self.x+50, self.x, dt=3/2),
                           rabbyt.lerp(self.x, self.x-50, dt=3/2, extend="reverse"),) 
  
  def update(self):
    #movement
    if self.mov_pat == 2:
      self.past_x = self.x
    elif self.at_pat == 0:
      self.y += self.speed
            
    elif self.at_pat == 1:     
      self.y -= 10

    elif self.at_pat == 2:     
      self.x += 2
      self.y += 2*self.speed

    self.past_x = self.x
    self.past_y = self.y

  def hone_in(self, centerx, centery):
    if self.at_pat == 3:
      difference = sqrt(((self.past_x-centerx)*(self.past_x-centerx))+(self.past_y-centery)*(self.past_y-centery))
      self.x = self.x-3*(self.past_x-centerx)/difference
      self.y = self.y-3*(self.past_y-centery)/difference
      self.past_x = self.x
      self.past_y = self.y
    
  def animate(self):
       #animation
       now = pygame.time.get_ticks() 
       delta = now - self.time_last
       constant = 90

       if delta > constant: 
           if self.frame < len(self.enemy_tex) - 1: 
               self.frame += 1 
	       self.tex_shape = self.enemy_tex[self.frame]
           else:
               self.frame = 0 
           self.time_last = now 

  def checkBounds(self):
    if self.x >= 350 or self.y >= 450 or self.x <= -350 or self.y <= -450:
      return True
    return False

  def freeze_Up(self, center):
    self.xy = center
    
  def render(self):
    rabbyt.Sprite.render(self)
