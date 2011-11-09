from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random
import settings
import player, enemy, bullet, chronos, Boss1
from settings import Font, FontSprite

def NameScreen(self, state_stack):
    backg = rabbyt.Sprite('1Menu_Screen1.png') 
    textbox = rabbyt.Sprite('1textbox.png')
    enter_name = FontSprite(self.font, "")
    enter_name.rgb = (0,0,0)
    textbox.y = -10

    self.done = False
    while not self.done:
        rabbyt.clear()
        backg.render()
        textbox.render()
        enter_name.render()

        self.clock.tick(40)

        for event in pygame.event.get():
            if event.type ==  QUIT:
                self.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(self.highScoreNames[i] + " " + str(self.highScores[i]) + "\n")

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.done = True
                    state_stack.append("Menu Screen")

                elif event.key == K_RETURN:
                    if(enter_name.text == ""):
                        self.winner_name = "Rabbit"
                    else:
		        self.winner_name = enter_name.text
                    self.done = True
                    state_stack.append("Level One")

                elif event.key == K_BACKSPACE:
                    enter_name.text = enter_name.text[:-1]
                    enter_name.x += 6

                elif not event.key == K_SPACE and len(enter_name.text) < 9:
                    enter_name.text += event.unicode
                    enter_name.x -= 6

        pygame.display.flip()

