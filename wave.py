## beginning of import
from __future__ import division
import pygame, rabbyt, sys
from math import cos, sin, radians, sqrt
import random
import os.path
import settings
import game_object

class Wave():
    def __init__(self, time):
        self.time = time
        self.elements = []
