## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings

def movpattern1(startx, starty):
    return rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=1),
                         rabbyt.lerp(startx+50, startx, dt=1),
                         rabbyt.lerp(startx, startx-50, dt=1, extend="reverse"),)

def pattern2(startx, starty):
    return rabbyt.chain( rabbyt.lerp(startx, startx-50, dt=1),
                         rabbyt.lerp(startx-50, startx, dt=1),
                         rabbyt.lerp(startx, startx+50, dt=1, extend="reverse"),)

def pattern3(startx, starty):    
     return (rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=3/2),
                           rabbyt.lerp(startx+50, startx, dt=3/2),
                           rabbyt.lerp(startx, startx-50, dt=3/2, extend="reverse"),)), \
                           (rabbyt.chain( rabbyt.lerp(self.y, self.y-300, dt=2),
                           rabbyt.lerp(self.y-300, self.y-150, dt=2),
                           rabbyt.lerp(self.y-150, self.y-450, dt=2),
                           rabbyt.lerp(self.y-450, self.y-400, dt=2),
                           rabbyt.lerp(self.y-400, self.y-1000, dt=2, extend="reverse"),))
