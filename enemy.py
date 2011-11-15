"""
Define ALL the enemies!
"""
## beginning of import
from __future__ import division
import pygame, rabbyt
import settings
import game_object

class Enemy(rabbyt.Sprite, game_object.GameObject):
    """Enemy class"""
    def __init__(self, screen, image_file, startx, starty, patternx, patterny):
        rabbyt.Sprite.__init__(self, image_file, (-91.7857143, \
                                                 74, 91.7857143, -74))
        game_object.GameObject.__init__(self)
        self.screen = screen
        self.frame = 0

        self.enemy_tex = settings.get_tex_shapes(self.tex_shape, \
                                                 int(image_file[:1]))

        #self.y = rabbyt.lerp(400, 0, dt=2, extend="reverse")
        self.time_last = pygame.time.get_ticks() 
        self.x = patternx(startx)
        self.y = patterny(starty)

        #self.offset = 74
   
    def animate(self):
        """animation method"""
        now = pygame.time.get_ticks() 
        delta = now - self.time_last
        constant = 90

        if delta > constant: 
            if self.frame < len(self.enemy_tex) - 1: 
                self.frame += 1 
                self.tex_shape = self.enemy_tex[self.frame]
            else:
                self.frame = 0 
            self.time_last = now 

    def checkBounds(self):
        """checkbounds method"""
        if self.x >= 450 or self.y <= -350 or self.x <= -450:
            return True
        return False

    def freeze_Up(self, center):
        """FREEZE"""
        self.xy = center
    
    def render(self):
        """rabbyt render method"""
        rabbyt.Sprite.render(self)
        
    def isOffMap(self):
        """checks if off method"""
        if self.y <= -350 or self.x >= 450 or self.x <= -450:
            return True
        else:
            return False

class Dragon(Enemy):
    """Dragons"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "7dragon.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 30
        self.health = 1
        self.damage = 1
        self.point_value = 50

class Dinosaur(Enemy):
    """Dinosaurs"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "5dino.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 30
        self.health = 3
        self.damage = 1
        self.point_value = 5000

class Plane(Enemy):
    """Planes"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "3ww2.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 30
        self.health = 4
        self.damage = 1
        self.point_value = 150

class Boss1(Enemy):
    """First Boss"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "1DragonBoss.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 80
        self.health = 50
        self.damage = 1
        self.point_value = 5000

class BossHands(Enemy):
    """Boss Hands"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "7Dragon.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 30
        self.health = 10
        self.damage = 1
        self.point_value = 5000

class Boss2(Enemy):
    """Second Boss"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "1DragonBoss.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 75
        self.health = 75
        self.damage = 1
        self.point_value = 5000
        
class Boss3(Enemy):
    """Third Boss"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "2boss3.png"
        Enemy.__init__(self, screen, image, startx, starty, patternx, patterny)

        #data individual to an enemy
        self.bounding_radius = 30
        self.health = 100
        self.damage = 1
        self.point_value = 5000
