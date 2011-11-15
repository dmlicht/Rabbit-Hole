"""
Player class
"""
## Imports ##
from __future__ import division
import pygame
import rabbyt
import settings
import bullet
import game_object

## BOOST CONSTANTS ##
BOOST_FUEL_COST = 1
BOOST_MAGNITUDE = 2
BOOST_REGENERATION_RATE = .5
MAXIMUM_BOOST_FUEL = 100

## TILT CONSTANTS ##
TILT_MAGNITUDE = 25
TILT_SPEED = .1

BULLET_VELOCITY = 2

STARTING_HEALTH = 5


class Ship(rabbyt.Sprite, game_object.GameObject):
    """Ship Class"""
    def __init__(self, name, screen):
        game_object.GameObject.__init__(self)
        rabbyt.Sprite.__init__(self, name+'.png', (-244/6.0, 51, 244/6.0, -51))
        self.screen = screen
        self.time_last = pygame.time.get_ticks() 

        self.acceleration_x = 0
        self.acceleration_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.tilt = 0
        self.boosting = False
        self.boost_fuel = 100.0

        self.offsetx = -51
        self.offsety = -244/6.0

        self.teleport_position_x = -1
        self.teleport_position_y = -1
        self.teleport_location_set = False

        self.has_fired = False

        self.frame = 0
        self.tex_shapes = settings.get_tex_shapes(self.tex_shape, int(name[:1]))

        #self.xy = (0,self.offsety*7)
        #self.velocity = [0,0]
        self.rot = 0
        self.health = STARTING_HEALTH
        self.bounding_radius = 30

    def update(self):
        """Update method"""
        #if setting_teleport_position: set_teleport_position()
        if self.boosting: 
            self.acceleration_boost()
        if self.boost_fuel < MAXIMUM_BOOST_FUEL:
            self.boost_fuel += BOOST_REGENERATION_RATE
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y
        self.velocity_x *= .9
        self.velocity_y *= .9
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rot = rabbyt.lerp(self.rot, (self.tilt * TILT_MAGNITUDE), \
                               dt=TILT_SPEED)

    def animate(self):
        """animates the ship"""
        now = pygame.time.get_ticks() 
        delta = now - self.time_last
        constant = 10

        if delta > constant: 
            if self.frame < len(self.tex_shapes) - 1: 
                self.frame += 1 
                self.tex_shape = self.tex_shapes[self.frame]
            else:
                self.frame = 0 
            self.time_last = now 

    def check_horizontal_bounds(self): 
        """Locks ship in horizontal bounds of screen"""
        if self.x > self.screen.get_width()/2 + self.offsetx:
            self.x = self.screen.get_width()/2 + self.offsetx
            return True
        if self.x < -self.screen.get_width()/2 - self.offsetx:
            self.x = -self.screen.get_width()/2 - self.offsetx
            return True
        return False

    def check_vertical_bounds(self): 
        """Locks ship in vertical bounds of screen"""
        if self.y > 300 + self.offsety - 15:
            self.y = 300 + self.offsety - 15
            return True
        if self.y < -self.screen.get_height()/2 - self.offsety + 15:
            self.y = -self.screen.get_height()/2 - self.offsety + 15
            return True
        return False

    def acceleration_boost(self):
        """Boosts ship"""
        self.boosting = False
        if self.boost_fuel > BOOST_FUEL_COST:
            self.boost_fuel -= BOOST_FUEL_COST
            self.acceleration_x *= BOOST_MAGNITUDE
            self.acceleration_y *= BOOST_MAGNITUDE

    def render(self):
        """Render method for rabbyt"""
        rabbyt.Sprite.render(self)

    def attemptfire(self):
        """Able to fire? (can't hold down shots)"""
        if self.has_fired:
            return False
        else:
            return self.fire()

    def fire(self):
        """Yay you can now fire"""
        new_bullet = bullet.Bullet(self.xy, self.rot, BULLET_VELOCITY)
        self.has_fired = True
        return new_bullet
