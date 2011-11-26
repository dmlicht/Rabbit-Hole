"""
Chronos energy
"""
## beginning of import
from __future__ import division
import pygame
import rabbyt

class Spark(rabbyt.Sprite):
    """Chronos Energy"""
    def __init__(self, screen, start_x, start_y):
        rabbyt.Sprite.__init__(self, '1energy.png')
        self.x = start_x
        end_y = start_y - 800
        self.y = rabbyt.lerp(start_y, end_y, dt=3)
        self.rot = rabbyt.lerp(0, 180, dt=2, extend="extrapolate")
        self.time_last = pygame.time.get_ticks() 
        self.screen = screen
 
    """
    def update(self):
        self.y += self.speed
        self.rot += 0.4
    """

    def isOffMap(self):
        """checks if off method"""
        if self.y <= -350 or self.x >= 450 or self.x <= -450:
            return True
        else:
            return False

    def checkBounds(self):
        """checks bounds"""
        if self.x >= 350 or self.y >= 450 or self.x <= -350 or self.y <= -450:
            return True
        return False
