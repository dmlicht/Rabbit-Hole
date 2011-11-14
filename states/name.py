from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random
import settings
import player, enemy, bullet, chronos, Boss1
from settings import Font, FontSprite
import state, states.menu

#def NameScreen(self, state_stack):
class Name(state.State):
  def run(self, game, state_stack):
    backg = rabbyt.Sprite('1Menu_Screen1.png') 
    textbox = rabbyt.Sprite('1textbox.png')
    enter_name = FontSprite(game.font, "")
    enter_name.rgb = (0,0,0)
    textbox.y = -10
    self.game = game

    game.done = False
    while not game.done:
        rabbyt.clear()
        backg.render()
        textbox.render()
        enter_name.render()

        game.clock.tick(40)

        for event in pygame.event.get():
            if event.type ==  QUIT:
                game.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(game.highScoreNames[i] + " " + str(game.highScores[i]) + "\n")

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.done = True
                    state_stack.append(states.menu.Menu())

                elif event.key == K_RETURN:
                    if(enter_name.text == ""):
                        game.winner_name = "Rabbit"
                    else:
		        game.winner_name = enter_name.text
                    game.done = True
                    state_stack.append(states.level.Level(self.game, "sample_wave_file.txt", states.cuttwo.CutTwo()))

                elif event.key == K_BACKSPACE:
                    enter_name.text = enter_name.text[:-1]
                    enter_name.x += 6

                elif not event.key == K_SPACE and len(enter_name.text) < 9:
                    enter_name.text += event.unicode
                    enter_name.x -= 6

        pygame.display.flip()