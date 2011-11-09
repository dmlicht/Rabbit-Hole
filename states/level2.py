from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands
from settings import Font, FontSprite
import level

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

MAX_FUEL = 100.0
FUEL_DRAIN = 10.0
MIN_FUEL = 0	
FUEL_REGAIN = .1

class Level2(level.Level):
    def run(self, game):
        background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, "sample_tile_layout2.txt")
        background.initialize()

        clock = pygame.time.Clock() 

        self.done = False

        while not self.done:
            if pygame.time.get_ticks() - game.fps > 1000:
                print "FPS: ", game.clock.get_fps()
                game.fps = pygame.time.get_ticks()

            self.handle_user_events()
            rabbyt.set_time(pygame.time.get_ticks()/1000.0)
            rabbyt.scheduler.pump()
            rabbyt.clear()

            #background handling
            background.maintain_tile_rows()
            self.ship.update()

            background.render()
            self.ship.render()
            self.text_score.render()
            self.text_boost.render()
            self.text_health.render()
            self.text_chronos.render()

            self.text_health.text = "Health: " + str(self.health)
            if self.fuel < MAX_FUEL:
                self.fuel += FUEL_REGAIN
                self.text_boost.text = "Boost Fuel: " + str(self.fuel)
            else:
                self.fuel = 100.0
                self.text_boost.text = "Boost Fuel: " + str(self.fuel)

            game.clock.tick(40)
            pygame.display.flip()
