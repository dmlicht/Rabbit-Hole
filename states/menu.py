from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *
import os, random
import settings
from settings import Font, FontSprite
import player, enemy, bullet, chronos, Boss1
import state, states.cut

RGB_UNSELECTED  = (255, 255, 255)
RGB_SELECTED    = (0, 0, 0)

START           = 0
SOUND           = 1
BRIGHTNESS      = 2
SCORE           = 3
QUIT            = 4

#def MenuScreen(game, state_stack):
class Menu(state.State):
    def run(self, game, state_stack):
        backg = rabbyt.Sprite('1Menu_Screen1.png') 
        self.menu_option = 0
        self.game = game
        self.state_stack = state_stack

        self.game.user.score = 0
        text_start = FontSprite(game.font, "Start Game")
        text_sound = FontSprite(game.font, "Adjust Sound")
        text_brightness = FontSprite(game.font, "Adjust Brightness")
        text_score = FontSprite(game.font, "High Scores")
        text_quit = FontSprite(game.font, "Quit")

        #set menu item positions
        text_start.xy = (-65, 100)
        text_sound.xy = (-80,50)
        text_brightness.xy = (-110,0)
        text_score.xy = (-77,-50)
        text_quit.xy = (-22,-100)        

        self.menu_items = [text_start, text_sound, text_brightness, text_score, text_quit]
        self.highlight()        

        game.done = False

        while not game.done:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pass
                    #self.quit()
                elif event.type == KEYDOWN:
                    self.key_press(event.key)

            rabbyt.clear()
            backg.render()
            text_start.render()
            text_sound.render()
            text_brightness.render()
            text_score.render()
            text_quit.render()

            pygame.display.flip()
            game.clock.tick(40)

    def quit(self):
        self.game.done = True
        fdata = open("RabbitHighScores", 'w')
        for i in range(5):
            fdata.write(self.game.highScoreNames[i] + " " + str(self.game.highScores[i]) + "\n")

    def key_press(self, key_pressed):
        if key_pressed == K_ESCAPE:
            self.esc_press()
        elif key_pressed == K_SPACE or key_pressed == K_RETURN:
            self.space_press()
        elif key_pressed == K_DOWN:
            self.down_press()
        elif key_pressed == K_UP:
            self.up_press()
        self.highlight()        

    def esc_press(self):
        self.game.done = True
        fdata = open("RabbitHighScores", 'w')
        for i in range(5):
            fdata.write(self.game.highScoreNames[i] + " " + str(self.game.highScores[i]) + "\n")
    
    def space_press(self):
        if self.menu_option == START:
            self.game.done = True
            self.state_stack.append(states.cut.Cut())
        elif self.menu_option == SOUND:
            self.game.done = False
        elif self.menu_option == BRIGHTNESS:
            self.game.done = False
        elif self.menu_option == SCORE:
            self.game.done = True
            self.state_stack.append(states.highscore.High())
        elif self.menu_option == QUIT:
            self.game.done = True
    
    def down_press(self):
        if self.menu_option < 4:
            self.menu_option += 1
        else:
            self.menu_option = 0

    def up_press(self):
        if self.menu_option > 0:
            self.menu_option -= 1
        else:
            self.menu_option = 4

    def highlight(self):
        for current_item in self.menu_items:
            current_item.rgb = RGB_UNSELECTED
        self.menu_items[self.menu_option].rgb = RGB_SELECTED
