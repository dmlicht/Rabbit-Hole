## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings

BOSS_Y_OFFSET = -50

class Boss_hand(rabbyt.Sprite):
  def __init__(self, name, screen, boss, y_pos, boss_x_offset):
    rabbyt.Sprite.__init__(self, name+'.png', (-91.7857143, 74, 91.7857143, -74))
    self.screen = screen
    self.frame = 0
    self.boss = boss
    self.boss_x_offset = boss_x_offset
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
    self.set_to_boss()
    #self.x = boss.attrgetter('x') + boss_x_offset
    #self.y = boss.attrgetter('y') + BOSS_Y_OFFSET
    self.past_x = self.x
    self.past_y = self.y

  def hone_in(self, ship):
    pass
    boss_attack_miss_factor = random.randint(0, 100)
    attack_x_position = ship.x + boss_attack_miss_factor
    self.xy = rabbyt.chain(
                    rabbyt.lerp((self.x , self.y), (boss_attack_miss_factor, ship.y), dt = 1),
                    rabbyt.lerp((self.x, self.y), (self.boss.x, self.boss.y), dt = 1))
    rabbyt.scheduler.add(self.set_to_boss, pygame.time.get_ticks()/1000 + 2)

  def set_to_boss(self):
    self.x = self.boss.attrgetter('x') + self.boss_x_offset
    self.y = self.boss.attrgetter('y') + BOSS_Y_OFFSET

    """
    difference = sqrt(((self.past_x-centerx)*(self.past_x-centerx))+(self.past_y-centery)*(self.past_y-centery))
    if not difference == 0:
      self.x = self.x-7*(self.past_x-centerx)/difference
      self.y = self.y-7*(self.past_y-centery)/difference
      self.past_x = self.x
      self.past_y = self.y
    """
  """  
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
  """

  """
  def checkBounds(self):
    if self.x > self.screen.get_width()/2:
            #self.x = self.screen.get_width()/2
            return True
    if self.x < -self.screen.get_width()/2:
            #self.x = -self.screen.get_width()/2
            return True
    return False
  """

  def freeze_Up(self, center):
    self.xy = center
    
  def render(self):
    rabbyt.Sprite.render(self)
