"""
Handles the waves of enemies
"""

import enemy
import os
import wave
import wave_element
import movement_pattern

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

class WaveHandler():
    """Handles the waves of enemies"""
    def __init__(self, level_file_path):
        self.waves = [] 
        self.level_file_path = level_file_path
        self.wave_index = 0
        self.layout_file_path = ""
        self.err_line = 0

    def parse_level_file(self):
        """Parses the level file"""
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
                        enemy_ = enemy_build_details[0]
                        startx = enemy_build_details[1]
                        starty = enemy_build_details[2]
                        patternx = enemy_build_details[3]
                        patterny = enemy_build_details[4]

                        usable_build_details = self.check_and_prepare_enemy( \
                                     enemy_, startx, starty, patternx, patterny)
                        if usable_build_details:
                            new_enemy_for_wave = wave_element.WaveElement( \
                                                      usable_build_details[0], 
                                                      usable_build_details[1], 
                                                      usable_build_details[2], 
                                                      usable_build_details[3],
                                                      usable_build_details[4])
                            new_wave.elements.append(new_enemy_for_wave)

                        inner_line = self.readline_with_debug(level_file)
                    self.waves.append(new_wave)
                    outer_line = self.readline_with_debug(level_file)

    def check_and_prepare_enemy(self, pre_e, pre_x, pre_y, pre_px, pre_py):
        """Checks and prepares enemies"""
        error_string = ""
        if not hasattr(enemy, pre_e):
            error_string = "Could not find requested enemy class"
        elif not is_convertable_to_integer(pre_x):
            error_string = "Non integer string used for startx"
        elif not is_convertable_to_integer(pre_y):
            error_string = "Non integer string used for starty"
        elif not hasattr(movement_pattern, pre_px):
            error_string = "Could not find requested movement pattern"
        elif not hasattr(movement_pattern, pre_py):
            error_string = "Could not find requested movement pattern"
        else:
            post_e = eval('enemy.' + pre_e)
            post_x = int(pre_x)
            post_y = int(pre_y)
            post_px = eval('movement_pattern.' + pre_px)
            post_py = eval('movement_pattern.' + pre_py)
            return post_e, post_x, post_y, post_px, post_py
        print 'line: ', self.err_line, ' - ', error_string
        return False

    def get_next_wave(self):
        """Next line of file"""
        if not self.all_waves_called():
            self.wave_index += 1
            return self.waves[self.wave_index - 1]
        else: 
            return False

    def get_wave_times(self):
        """When to start/stop"""
        wave_times = []
        for wave_ in self.waves:
            wave_times.append(wave_.time)
        return wave_times

    def all_waves_called(self):
        """Are we done?"""
        if self.wave_index < len(self.waves):
            return False
        else:
            return True

    def readline_with_debug(self, level_file):
        """Debugging method"""
        self.err_line += 1
        return level_file.readline()
    
def is_convertable_to_integer(number):
    """Method to find out if is convertable to int"""
    try:
        int(number)
        return True
    except ValueError:
        return False
