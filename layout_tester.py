## Imports ##
from __future__ import division
import pygame, rabbyt
from math import cos, sin, radians
import random
import os.path
import settings
import layout

test_layout = layout.Layout("sample_tile_parser.txt")
print test_layout.get_next_row()
