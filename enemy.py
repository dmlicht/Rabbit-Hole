## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings
import game_object

class Enemy(rabbyt.Sprite, game_object.GameObject):
    def __init__(self, screen, image_file, startx, starty, patternx, patterny):
        rabbyt.Sprite.__init__(self, image_file, (-91.7857143, 74, 91.7857143, -74))
        game_object.GameObject.__init__(self)
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

        #self.y = rabbyt.lerp(400, 0, dt=2, extend="reverse")
        self.time_last = pygame.time.get_ticks() 
        self.x = patternx(startx)
        self.y = patterny(starty)

        #self.offset = 74
   
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

class Dragon(Enemy):
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "7dragon.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 30
        self.health = 1
        self.damage = 1

