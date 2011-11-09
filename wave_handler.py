import pygame, rabbyt, sys
from pygame.locals import *

import os
import tiles, layout
import settings
import player, enemy, Boss1, Boss0, BossHands
import wave, wave_element, movement_pattern

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

class WaveHandler():
    def __init__(self, level_file_path):
        self.waves = [] 
        self.level_file_path = level_file_path
        self.wave_index = 0
        self.layout_file_path = ""

    def parse_level_file(self):
        time = 0
        enemies = []
        if not os.path.isfile(self.level_file_path):
            return False
        else:
            level_file = open(self.level_file_path)
            outer_line = level_file.readline()
            while not (outer_line == ""):
                if outer_line == "\n":
                    outer_line = level_file.readline()

                elif outer_line.split()[0] == "layout:":
                    inner_line = level_file.readline()
                    self.layout_file_path = inner_line.split()[0]
                    outer_line = level_file.readline()

                #if a number is read in
                else: 
                    wave_call_time = outer_line.split()[0]
                    new_wave = wave.Wave(int(wave_call_time))
                    inner_line = level_file.readline()
                    while not (inner_line == "$end\n"):
                        enemy_build_details = inner_line.split()
                        enemy = enemy_build_details[0]
                        startx = enemy_build_details[1]
                        starty = enemy_build_details[2]
                        pattern = enemy_build_details[3]

                        usable_build_details = self.check_and_prepare_enemy(enemy, startx, starty, pattern)
                        if usable_build_details:
                            new_enemy_for_wave = wave_element.WaveElement(usable_build_details[0], 
                                                                          usable_build_details[1], 
                                                                          usable_build_details[2], 
                                                                          usable_build_details[3])
                            new_wave.elements.append(new_enemy_for_wave)

                        inner_line = level_file.readline()
                    self.waves.append(new_wave)
                    outer_line = level_file.readline()

    def check_and_prepare_enemy(self, pre_enemy, pre_startx, pre_starty, pre_pattern):
        error_string = ""
        if not hasattr(enemy, pre_enemy):
            error_string = "Could not find requested enemy class"
        elif not is_convertable_to_integer(pre_startx):
            error_string = "Non integer string used for startx"
        elif not is_convertable_to_integer(pre_starty):
            error_string = "Non integer string used for starty"
        elif not hasattr(movement_pattern, pre_pattern):
            error_string = "Could not find requested movement pattern"
        else:
            post_enemy = eval('enemy.' + pre_enemy)
            post_startx = int(pre_startx)
            post_starty = int(pre_starty)
            post_pattern = eval('movement_pattern.' + pre_pattern)
            return post_enemy, post_startx, post_starty, post_pattern
        print error_string, 'please recheck level text file'
        return False

    def get_next_wave(self):
        if self.wave_index < len(self.waves):
            self.wave_index += 1
            return self.waves[self.wave_index - 1]
        else: 
            return False

    def get_wave_times(self):
        wave_times = []
        for wave in self.waves:
            wave_times.append(wave.time)
        return wave_times

def is_convertable_to_integer(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
