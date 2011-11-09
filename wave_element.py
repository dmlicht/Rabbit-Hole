## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings
import game_object

class WaveElement():
    def __init__(self, enemy_type, startx, starty, pattern):
        self.enemy_type = enemy_type
        self.startx = startx
        self.starty = starty
        self.pattern = pattern
