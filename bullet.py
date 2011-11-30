"""
Bullet class
"""
## beginning of import
from __future__ import division
import rabbyt

from math import cos, sin, radians
import game_object

#rabbyt.data_directory = os.path.dirname(__file__)
#rabbyt.set_default_attribs()

## end of import

#rabbyt.set_viewport((800,600))

class Bullet(rabbyt.Sprite, game_object.GameObject): 
    """Bullet class"""
    def __init__(self, start, angle, speed):
        rabbyt.Sprite.__init__(self, '1rock_bullet.png')
        game_object.GameObject.__init__(self)
        self.xy = start
        self.rot = angle
        self.speed = speed
        self.bounding_radius = 16
        self.health = 1
        self.damage = 1

        x_end_position = cos(radians(self.rot+90)) * 1000 + start[0]
        y_end_position = sin(radians(self.rot+90))* 1000 + start[1]
        self.xy = rabbyt.lerp(start, (x_end_position, y_end_position), dt=speed)

    def update(self): 
        """update method"""
        self.x += cos(radians(self.rot+90))*self.speed
        self.y += sin(radians(self.rot+90))*self.speed

    def isOffMap(self):
        """Checks bounds"""
        if self.x >= 500 or self.y >= 450 or self.x <= -500 or self.y <= -450:
            return True
        return False