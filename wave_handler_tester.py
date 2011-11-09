from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands, dragon
from settings import Font, FontSprite
import wave, wave_element, wave_handler

level_waves = wave_handler.WaveHandler("sample_wave_file2.txt")
level_waves.parse_level_file()
current_wave = level_waves.get_next_wave()
while current_wave:
    print 'wave time: ', current_wave.time
    for element in current_wave.elements:
        print 'enemy type: ', element.enemy_type
        print 'start x position: ', element.startx
        print 'start y position: ', element.starty
        print 'pattern: ', element.pattern
    current_wave = level_waves.get_next_wave()
