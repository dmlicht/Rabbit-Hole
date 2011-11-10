## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings

def movpatternx(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=1),
                         rabbyt.lerp(startx+50, startx, dt=1),
                         rabbyt.lerp(startx, startx-200, dt=1, extend="reverse"),)

def movpatterny(start):
    return rabbyt.chain( rabbyt.ease(start, start-400, dt=1),
                         rabbyt.ease(start-400, start-200, dt=2),
                         rabbyt.ease(start-200, start-400, dt=1, extend="reverse"),)

def pattern3(startx, starty):    
     return (rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=3/2),
                           rabbyt.lerp(startx+50, startx, dt=3/2),
                           rabbyt.lerp(startx, startx-50, dt=3/2, extend="reverse"),)), \
                           (rabbyt.chain( rabbyt.lerp(self.y, self.y-300, dt=2),
                           rabbyt.lerp(self.y-300, self.y-150, dt=2),
                           rabbyt.lerp(self.y-150, self.y-450, dt=2),
                           rabbyt.lerp(self.y-450, self.y-400, dt=2),
                           rabbyt.lerp(self.y-400, self.y-1000, dt=2, extend="reverse"),))
