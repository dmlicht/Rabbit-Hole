"""
Name State
"""
from __future__ import division
import pygame
import rabbyt

from settings import FontSprite
import state
import states.menu

LEVEL_TO_RUN = "level1.txt"

class Name(state.State):
    """Name State"""
    def run(self, game, state_stack):
        backg = rabbyt.Sprite('1Menu_Screen1.png') 
        textbox = rabbyt.Sprite('1textbox.png')
        enter_name = FontSprite(game.font, "")
        inst = FontSprite(game.font, "Instructions:")
        inst.rgb = (0, 0, 0)
        inst.y = -50
        inst.x = -90
        movement = FontSprite(game.font, "Move with the arrow keys")
        movement.x = -150
        movement.y = -100
        movement.rgb = (0, 0, 0)
        fire = FontSprite(game.font, "Press the Space Bar to fire")
        fire.x = -150
        fire.y = -150
        fire.rgb = (0, 0, 0)
        save = FontSprite(game.font, "Press the C key to save a time to")
        save.x = -400
        save.y = -200
        save.rgb = (10, 10, 10)
        save2 = FontSprite(game.font, "go back to and help yourself")
        save2.x = -400
        save2.y = -250
        save2.rgb = (150, 150, 150)
        revert = FontSprite(game.font, "Press the C again key to go back ")
        revert.x = 50
        revert.y = -200
        revert.rgb = (100, 100, 100)
        revert2 = FontSprite(game.font, "to the time you saved before.")
        revert2.x = 25
        revert2.y = -250
        revert2.rgb = (150, 150, 150)
        enter_name.rgb = (0, 0, 0)
        textbox.y = -10
        self.game = game

        game.done = False
        while not self.game.done:
            rabbyt.clear()
            backg.render()
            textbox.render()
            enter_name.render()
            inst.render()
            movement.render()
            fire.render()
            save.render()
            save2.render()
            revert.render()
            revert2.render()

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
                        self.set_next_level(state_stack)

                    elif event.key == pygame.K_BACKSPACE:
                        enter_name.text = enter_name.text[:-1]
                        enter_name.x += 6

                    elif not event.key == pygame.K_SPACE and \
                        len(enter_name.text) < 9:
                        enter_name.text += event.unicode
                        enter_name.x -= 6
                    
                elif event.type == pygame.JOYBUTTONDOWN:
                    if self.game.joystick.get_button(self.game.controls.settings["Escape"]):
                        self.game.done = True
                        state_stack.append(states.menu.Menu())
                    if self.game.joystick.get_button(self.game.controls.settings["Fire"]):
                        if(enter_name.text == ""):
                            self.game.winner_name = "Rabbit"
                        else:
                            self.game.winner_name = enter_name.text
                        self.game.done = True
                        self.set_next_level(state_stack)

            pygame.display.flip()

    def set_next_level(self, state_stack):                        
        state_stack.append(states.level.Level(self.game, LEVEL_TO_RUN, states.cuttwo.CutTwo()))
