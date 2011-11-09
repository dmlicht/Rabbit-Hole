import pygame, rabbyt, sys
from pygame.locals import *

import os
import tiles, layout
import settings
import player, enemy, Boss1, Boss0, BossHands
import level

class WaveHandler():
    def __init__(self, levelname):
        self.waves = [] 
        self.levelname = levelname
        self.wave_index = 0

    def parse_level_file(self):
        time = 0
        enemies = []
        if not os.path.isfile(self.levelname)
            return False
        else:
            level_file = open(levelname)
            next_line = level_file.readline()
            while not (next_line == ""):
                if next_line[0] == 'a':
                    self.background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, next_line[2:] + ".txt")
                elif next_line[0] == '0':    
                    time = int(nextline[2:])
                elif next_line[0] == '1':
                    parts = next_line.split()
                    enemies.append(wave_element(parts[1], parts[2], parts[3], parts[4]))
                elif next_line[0] == '2':
                    self.waves.append(time, enemies)
                    time = 0
                    for i in range(len(enemies)-1):
                        enemies.pop()

    def Set_Up_Wave(self, wave_n):
        for i in wave_n.attackers:
            self.enemies.append(enemy(i.image, i.at_pat, 0, i.x_pos, i.y_pos))

    def get_next_wave(self):
        if self.wave_index < len(self.waves):
            self.wave_index += 1
            return self.waves[self.wave_index - 1]
        else: return False
"""        
class wave_element():
    def __init__(self, image, x_pos, y_pos, at_pat):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.at_pat = at_pat
        
class wave():
    def __init__(self, time, attackers):
        self.time = time
        self.attackers = attackers
"""
