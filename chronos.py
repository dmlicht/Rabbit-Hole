"""
Chronos energy
"""
## beginning of import
from __future__ import division
import pygame, rabbyt

class Spark(rabbyt.Sprite):
    """Chronos Energy"""
    def __init__(self, screen, xy):
        rabbyt.Sprite.__init__(self, '1energy.png')
  
        self.speed = -3
        self.xy = xy
        self.rot = 0

        self.time_last = pygame.time.get_ticks() 
        self.screen = screen
 
    def update(self):
        """update method"""
        self.y += self.speed
        self.rot += 0.4

    def checkBounds(self):
        """checks bounds"""
        if self.x >= 350 or self.y >= 450 or self.x <= -350 or self.y <= -450:
            return True
        return False
