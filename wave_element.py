## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings
import game_object

class WaveElement():
    def __init__(self, startx, starty, pattern, sprite):
        self.startx = startx
        self.starty = starty
        self.pattern = pattern
        self.sprite = sprite
