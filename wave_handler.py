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
        self.err_line = 0

    def parse_level_file(self):
        time = 0
        enemies = []
        if not os.path.isfile(self.level_file_path):
            return False
        else:
            level_file = open(self.level_file_path)
            outer_line = self.readline_with_debug(level_file)
            while not (outer_line == ""):
                if outer_line == "\n":
                    outer_line = self.readline_with_debug(level_file)

                elif outer_line.split()[0] == "layout:":
                    inner_line = self.readline_with_debug(level_file)
                    self.layout_file_path = inner_line.split()[0]
                    outer_line = self.readline_with_debug(level_file)

                #if a number is read in
                else: 
                    wave_call_time = outer_line.split()[0]
                    new_wave = wave.Wave(int(wave_call_time))
                    inner_line = self.readline_with_debug(level_file)
                    while not (inner_line == "$end\n"):
                        enemy_build_details = inner_line.split()
                        enemy = enemy_build_details[0]
                        startx = enemy_build_details[1]
                        starty = enemy_build_details[2]
                        patternx = enemy_build_details[3]
                        patterny = enemy_build_details[4]

                        usable_build_details = self.check_and_prepare_enemy(enemy, startx, starty, patternx, patterny)
                        if usable_build_details:
                            new_enemy_for_wave = wave_element.WaveElement(usable_build_details[0], 
                                                                          usable_build_details[1], 
                                                                          usable_build_details[2], 
                                                                          usable_build_details[3],
                                                                          usable_build_details[4])
                            new_wave.elements.append(new_enemy_for_wave)

                        inner_line = self.readline_with_debug(level_file)
                    self.waves.append(new_wave)
                    outer_line = self.readline_with_debug(level_file)

    def check_and_prepare_enemy(self, pre_enemy, pre_startx, pre_starty, pre_patternx, pre_patterny):
        error_string = ""
        if not hasattr(enemy, pre_enemy):
            error_string = "Could not find requested enemy class"
        elif not is_convertable_to_integer(pre_startx):
            error_string = "Non integer string used for startx"
        elif not is_convertable_to_integer(pre_starty):
            error_string = "Non integer string used for starty"
        elif not hasattr(movement_pattern, pre_patternx):
            error_string = "Could not find requested movement pattern"
        elif not hasattr(movement_pattern, pre_patterny):
            error_string = "Could not find requested movement pattern"
        else:
            post_enemy = eval('enemy.' + pre_enemy)
            post_startx = int(pre_startx)
            post_starty = int(pre_starty)
            post_patternx = eval('movement_pattern.' + pre_patternx)
            post_patterny = eval('movement_pattern.' + pre_patterny)
            return post_enemy, post_startx, post_starty, post_patternx, post_patterny
        print 'line: ', self.err_line, ' - ', error_string
        return False

    def get_next_wave(self):
        if not self.all_waves_called():
            self.wave_index += 1
            return self.waves[self.wave_index - 1]
        else: 
            return False

    def get_wave_times(self):
        wave_times = []
        for wave in self.waves:
            wave_times.append(wave.time)
        return wave_times

    def all_waves_called(self):
        if self.wave_index < len(self.waves):
            return False
        else:
            return True

    def readline_with_debug(self, level_file):
        self.err_line += 1
        return level_file.readline()
    
def is_convertable_to_integer(number):
    try:
        int(number)
        return True
    except ValueError:
        return False
