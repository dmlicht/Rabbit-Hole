"""
Name State
"""
from __future__ import division
import pygame
import rabbyt

from settings import FontSprite
import state
import states.menu

class Name(state.State):
    """Name State"""
    def run(self, game, state_stack):
        backg = rabbyt.Sprite('1Menu_Screen1.png') 
        textbox = rabbyt.Sprite('1textbox.png')
        enter_name = FontSprite(game.font, "")
        enter_name.rgb = (0, 0, 0)
        textbox.y = -10
        self.game = game

        game.done = False
        while not self.game.done:
            rabbyt.clear()
            backg.render()
            textbox.render()
            enter_name.render()

            self.game.clock.tick(40)

            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    self.game.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(self.game.high_score_names[i] + " " + \
                        str(self.game.high_scores[i]) + "\n")

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.done = True
                        state_stack.append(states.menu.Menu())

                    elif event.key == pygame.K_RETURN:
                        if(enter_name.text == ""):
                            self.game.winner_name = "Rabbit"
                        else:
                            self.game.winner_name = enter_name.text
                        self.game.done = True
                        state_stack.append(states.level.Level(self.game, \
                        "level1.txt", states.cuttwo.CutTwo()))

                    elif event.key == pygame.K_BACKSPACE:
                        enter_name.text = enter_name.text[:-1]
                        enter_name.x += 6

                    elif not event.key == pygame.K_SPACE and \
                        len(enter_name.text) < 9:
                        enter_name.text += event.unicode
                        enter_name.x -= 6

            pygame.display.flip()
