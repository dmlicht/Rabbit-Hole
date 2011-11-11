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
def movpatternx1(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=1),
                         rabbyt.lerp(startx+50, startx-50, dt=1),
                         rabbyt.lerp(startx-50, startx, dt=1, extend="reverse"),)

def movpatterny1(start):
    return rabbyt.chain( rabbyt.lerp(start, start-600, dt=2),
                         rabbyt.lerp(start-600, start-500, dt=1),
                         rabbyt.lerp(start-500, start-800, dt=2, extend="reverse"),)
def movpatternx2(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+100, dt=1.5),
                         rabbyt.lerp(startx+100, startx-100, dt=3),
                         rabbyt.lerp(startx-100, startx, dt=1.5, extend="reverse"),)

def movpatterny2(start):
    return rabbyt.chain( rabbyt.lerp(start, start-400, dt=4),
                         rabbyt.lerp(start-400, start, dt=4, extend="reverse"),)

def movpattern_circx(startx):
    return startx+rabbyt.chain( rabbyt.lerp(0, 100, dt=1),
                         rabbyt.lerp(100, -100, dt=2),
                         rabbyt.lerp(-100, 0, dt=1, extend="reverse"),)

def movpattern_circy(start):
    return start+rabbyt.chain( rabbyt.lerp(-100, 0, dt=1),
                         rabbyt.lerp(0, 100, dt=1),
                         rabbyt.lerp(100, -100, dt=2, extend="reverse"),)

def pattern3(startx, starty):    
     return (rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=3/2),
                           rabbyt.lerp(startx+50, startx, dt=3/2),
                           rabbyt.lerp(startx, startx-50, dt=3/2, extend="reverse"),)), \
                           (rabbyt.chain( rabbyt.lerp(self.y, self.y-300, dt=2),
                           rabbyt.lerp(self.y-300, self.y-150, dt=2),
                           rabbyt.lerp(self.y-150, self.y-450, dt=2),
                           rabbyt.lerp(self.y-450, self.y-400, dt=2),
                           rabbyt.lerp(self.y-400, self.y-1000, dt=2, extend="reverse"),))
