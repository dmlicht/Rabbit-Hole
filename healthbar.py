"""
Bar class
"""
from __future__ import division
import rabbyt

class HealthBar():
    """Health bar for player"""
    def __init__(self):
        self.healthbar = rabbyt.Sprite(0, (0, 20, 190, 0))
        self.healthbar.rgb  = (34, 139, 34)
        self.healthbar.xy = (200, -240)

    def hit(self):
        """decreases health of bar"""
        if self.healthbar.shape[2][0] > 0:
            temp = self.healthbar.shape
            self.healthbar.shape = (0, temp[1][1], temp[2][0]-38, 0)

    def render(self):
        """render method"""
        self.healthbar.render()