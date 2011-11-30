"""
Define ALL the enemies!
"""
## beginning of import
from __future__ import division
import pygame
import rabbyt
import settings
import game_object
import random
import chronos
import bullet

class Enemy(rabbyt.Sprite, game_object.GameObject):
    """Enemy class"""
    def __init__(self, screen, image_file, startx, starty, patternx, patterny):
        rabbyt.Sprite.__init__(self, image_file, (-91.7857143, \
                                                 74, 91.7857143, -74))
        game_object.GameObject.__init__(self)
        self.screen = screen
        self.frame = 0

        if image_file == "5dino.png":
            self.shape = (-29.7, 26.5, 29.7, -26.5) 

        self.enemy_tex = settings.get_tex_shapes(self.tex_shape, \
                                                 int(image_file[:1]))

        #self.y = rabbyt.lerp(400, 0, dt=2, extend="reverse")
        self.time_last = pygame.time.get_ticks() 
        self.x = patternx(startx)
        self.y = patterny(starty)
        self.drop_rate = 10

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

    def die(self, level):
        """Method to handle item drops, generate death images and sounds
        and end the level with the boss"""

        drop = random.randint(0, self.drop_rate)
        if drop == 0:
            new_item = chronos.Spark(level.game.screen, self.x, self.y)
            level.items.append(new_item)
        return self.point_value

        
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
        self.fire_wait = 200
        self.wait = 0
        self.bullet_velocity = 2

    def fire(self, level):
        if self.wait == self.fire_wait:
            new_enemy_bullet = bullet.Bullet(self.xy, (self.rot + 180), self.bullet_velocity)
            level.enemy_bullets.append(new_enemy_bullet)
            self.wait = 0
        else: self.wait += 1

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
        self.health = 25
        self.damage = 1
        self.point_value = 5000

    def die(self, level):
        """Method to handle item drops, generate death images and sounds
        and end the level with the boss"""

        level.boss_dead = True
        return self.point_value

class BossHands(Enemy):
    """Boss Hands"""
    def __init__(self, screen, startx, starty, patternx, patterny):
        image = "7dragon.png"
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
        self.health = 30
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