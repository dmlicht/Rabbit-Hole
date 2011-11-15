"""
Wave Element class
"""

## beginning of import
from __future__ import division

class WaveElement():
    """Wave Element class"""
    def __init__(self, enemy_type, startx, starty, patternx, patterny):
        self.enemy_type = enemy_type
        self.startx = startx
        self.starty = starty
        self.patternx = patternx
        self.patterny = patterny
