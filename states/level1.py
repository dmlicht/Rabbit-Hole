from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands, dragon
from settings import Font, FontSprite
import level

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

MAX_FUEL = 100.0
FUEL_DRAIN = 10.0
MIN_FUEL = 0	
FUEL_REGAIN = .1

class Level1(level.Level):
    def run(self, game):
        self.background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, "sample_tile_layout.txt")
        self.background.initialize()

        self.done = False
        dragons = []
        #self.add_wave()
        rabbyt.scheduler.add(5, self.add_wave)
        rabbyt.scheduler.add(10, self.add_wave)
        self.game = game

        ##########
        """
        for i in range(10):
            dragon = enemy.Dragon("7dragon", self.screen, 3, 0, (i*800.0/10 - 400)) #random.randint(0,2))
            self.dragons.append(dragon)
        self.enT += self.enTimer.tick()
        if self.numEnemies >= 100 and not self.boss_out:
              self.boss0 = Boss0.Boss_zero(self.screen)
              self.boss_h1 = BossHands.Boss_hand('7dragon', self.screen, self.boss0, self.boss0.y, 75)
              self.boss_h2 = BossHands.Boss_hand('7dragon', self.screen, self.boss0, self.boss0.y, -75)
              self.final = [self.boss0, self.boss_h1, self.boss_h2]
              self.boss_out = True

        if self.bEnemy and self.enT > self.oldT + lev1time and not self.numEnemies >= 100:
              self.oldT = self.enT
              self.bEnemy = False
 
        if not self.bEnemy and not self.boss_out and not self.bFreeze:
          self.bEnemy= True
          self.numEnemies += 5
          for i in range(5):
                if pat_num >= len(lev1atpatterns)-1:
                    pat_num = 0
                dragon = enemy.Dragon("7dragon", self.screen, lev1atpatterns[pat_num], lev1movpatterns[pat_num], (i*800.0/5 - 400)) #random.randint(0,2))
                    #dragon = enemy.Dragon("7dragon", self.screen, random.randint(0,2))
                self.dragons.append(dragon)
          pat_num += 1
        """
        ##########

        while not self.done:
            self.handle_collisions_between(self.ship, self.enemies)
            self.handle_collisions_between(self.bullets, self.enemies)
            self.continue_level()
            if pygame.time.get_ticks() > 100000:
                self.done = True
                self.state_stack.append("Cut Two")

    def add_wave(self):
        for i in range(5):
            self.enemies.append(dragon.Dragon("7dragon", self.game.screen, -200 + i*100))

def scheduler_test():
    print 'did it work'
