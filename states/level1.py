from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands, dragon
from settings import Font, FontSprite
import level
import wave_handler, wave, wave_element
import movement_pattern

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

MAX_FUEL = 100.0
FUEL_DRAIN = 10.0
MIN_FUEL = 0	
FUEL_REGAIN = .1

class Level1(level.Level):
    def run(self, game):
        self.wave_builder = wave_handler.WaveHandler("sample_wave_file2.txt")
        self.wave_builder.parse_level_file()

        self.background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, self.wave_builder.layout_file_path)
        self.background.initialize()

        self.done = False
        dragons = []
        self.set_scheduler()
        self.game = game

        while not self.done:
            self.handle_collisions_between(self.ship, self.enemies)
            self.handle_collisions_between(self.bullets, self.enemies)
            self.continue_level()
            if pygame.time.get_ticks() > 100000:
                self.done = True
                self.state_stack.append("Cut Two")

    def set_scheduler(self):
        for time in self.wave_builder.get_wave_times():
            print time
            rabbyt.scheduler.add(time, self.build_wave)

    def build_wave(self):
        current_wave = self.wave_builder.get_next_wave()
        for element in current_wave.elements:
            new_enemy = element.enemy_type("7dragon", self.game.screen, element.startx)
            self.enemies.append(new_enemy)
