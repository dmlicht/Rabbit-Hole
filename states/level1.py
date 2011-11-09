from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands
from settings import Font, FontSprite
import level
import wave_handler, wave, wave_element
import movement_pattern

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

class Level1(level.Level):
    """
    def run(self, game):
        self.done = False
        self.set_scheduler()
        self.game = game

        while not self.done:
            self.handle_collisions_between(self.ship, self.enemies)
            self.handle_collisions_between(self.bullets, self.enemies)
            self.continue_level()
            if pygame.time.get_ticks() > 100000:
                self.done = True
                self.state_stack.append("Cut Two")
    """
