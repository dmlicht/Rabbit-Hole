from __future__ import division
import pygame
import rabbyt

import user_settings
from settings import FontSprite
import state
import states.menu

LEVEL_TO_RUN = "level1.txt"

class SetControls(state.State):
    def run(self, game, state_stack):
        backg = rabbyt.Sprite('1Menu_Screen1.png') 
        self.actions = ["Up", "Down", "Left", "Right", "Fire", "Tilt left", "Tilt right", "Boost", "Toggle time travel", "Skip", "Escape"]
        self.index = 0
        self.instruction_text = FontSprite(game.font, "Press the key you would like to correspond to the given action")
        self.instruction_text.x = -380
        self.instruction_text.y = 100
        self.action_text = FontSprite(game.font, self.actions[self.index])
        self.action_text.x = -380
        self.game = game

        game.controls = user_settings.UserSettings()

        game.done = False
        while not self.game.done:
            rabbyt.clear()
            backg.render()
            self.action_text.render()
            self.instruction_text.render()

            self.game.clock.tick(40)

            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    self.game.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(self.game.high_score_names[i] + " " + \
                        str(self.game.high_scores[i]) + "\n")
                elif event.type == pygame.locals.JOYBUTTONDOWN: # 10
                    print 'button down'
                    game.controls.settings[self.actions[self.index]] = event.button
                    self.index += 1
                    if self.index >= len(self.actions):
                        print game.controls.settings
                        game.done = True
                        break
                    self.action_text = FontSprite(game.font, self.actions[self.index])
                    self.action_text.x = -380
                    print self.index
                    print len(self.actions)
            pygame.display.flip()

    def set_next_level(self, state_stack):                        
        state_stack.append(states.level.Level(self.game, LEVEL_TO_RUN, states.cuttwo.CutTwo()))