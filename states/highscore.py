"""
High scores
"""
from __future__ import division
import pygame
import rabbyt

import state
import states.menu
from settings import Font, FontSprite

class High(state.State):
    """High Score Table"""
    def run(self, game, state_stack):
        header = rabbyt.Sprite('1bunny3.png')
        font = Font(pygame.font.Font(None, 80))
        name_list = []
        score_list = []

        for i in range(5):
            temp = FontSprite(font, str(game.high_score_names[i]))
            temp2 = FontSprite(font, str(game.high_scores[i]))
            temp.rgb = (255, 255, 255)
            temp2.rgb = (255, 255, 255)
            temp.xy = (-220, 87 - 55*i)
            temp2.xy = (150, 87 - 55*i)
            name_list.append(temp)
            score_list.append(temp2)

        game.done = False
        while not game.done:
            rabbyt.clear()
            header.render()

            for name, score in zip(name_list, score_list):
                name.render()
                score.render()

            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    game.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(game.high_score_names[i] + " " + \
                        str(game.high_scores[i]) + "\n")

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == \
                        pygame.K_RETURN:
                        game.done = True
                        state_stack.append(states.menu.Menu())
                elif event.type == pygame.JOYBUTTONDOWN and game.joystick.get_button(12):
                    game.done = True
                    state_stack.append(states.menu.Menu())

            game.clock.tick(40)

            pygame.display.flip()
