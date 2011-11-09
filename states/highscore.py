from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random
import settings
import player, enemy, bullet, chronos, Boss1
from settings import Font, FontSprite

def HighScreen(self, state_stack):
    header = rabbyt.Sprite('1bunny3.png')
    font = Font(pygame.font.Font(None, 80))
    name_list = []
    score_list = []

    for i in range(5):
        temp = FontSprite(font, str(self.highScoreNames[i]))
        temp2 = FontSprite(font, str(self.highScores[i]))
        temp.rgb = (255,255,255)
        temp2.rgb = (255,255,255)
        temp.xy = (-220, 87 - 55*i)
        temp2.xy = (150, 87 - 55*i)
        name_list.append(temp)
        score_list.append(temp2)

    self.done = False
    while not self.done:
        rabbyt.clear()
	header.render()

        for name, score in zip(name_list, score_list):
	    name.render()
            score.render()

        for event in pygame.event.get():
            if event.type ==  QUIT:
                self.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(self.highScoreNames[i] + " " + str(self.highScores[i]) + "\n")

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    self.done = True
                    state_stack.append("Menu Screen")

        self.clock.tick(40)

        pygame.display.flip()
