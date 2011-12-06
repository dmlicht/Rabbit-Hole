"""menu state for rabbit hole"""
from __future__ import division
import pygame, rabbyt
#from pygame.locals import *
from pygame.locals import K_SPACE, K_ESCAPE, K_RETURN, \
                            K_UP, K_DOWN, KEYDOWN, QUIT
from settings import FontSprite
import state, states.cut, states.instructions, states.highscore

RGB_UNSELECTED  = (120, 0, 0)
RGB_SELECTED    = (0, 0, 0)

START           = 0
INSTRUCT        = 1
SCORE           = 2
QUIT            = 3

#def MenuScreen(game, state_stack):
class Menu(state.State):
    """manages state choices"""
    def __init__(self):
        pass
    def run(self, game, state_stack):
        """starts the menu state"""
        backg = rabbyt.Sprite('1Menu_Screen1.png') 
        self.game = game
        self.state_stack = state_stack
        self.menu_option = 0

        self.game.user.score = 0
        text_start = FontSprite(game.font, "Start Game")
        text_instruct = FontSprite(game.font, "Instructions")
        text_score = FontSprite(game.font, "High Scores")
        text_quit = FontSprite(game.font, "Quit")

        #set menu item positions
        text_start.xy = (-65, 100)
        text_instruct.xy = (-70, 50)
        text_score.xy = (-70, 0)  
        text_quit.xy = (-19, -50) 

        self.menu_items = [ text_start, \
			    text_instruct, \
                            text_score, \
                            text_quit]

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
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.handle_joy()

            rabbyt.clear()
            backg.render()
            text_start.render()
            text_instruct.render()
            text_score.render()
            text_quit.render()

            pygame.display.flip()
            game.clock.tick(40)

    def quit(self):
        """has user exit game"""
        self.game.done = True
        fdata = open("RabbitHighScores", 'w')
        for i in range(5):
            fdata.write(self.game.high_score_names[i] + " " + \
                    str(self.game.high_scores[i]) + "\n")

    def handle_joy(self):
        joy = self.game.joystick
        if joy.get_button(self.game.controls.settings["Escape"]): self.esc_press()
        elif joy.get_button(self.game.controls.settings["Fire"]): self.space_press()
        elif joy.get_button(self.game.controls.settings["Down"]): self.down_press()
        elif joy.get_button(self.game.controls.settings["Up"]): self.up_press()
        self.highlight()

    def key_press(self, key_pressed):
        """delegates key presses to specific key functions
        then highlights currently selected option"""
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
        """handles pressing escape key"""
        self.game.done = True
        fdata = open("RabbitHighScores", 'w')
        for i in range(5):
            fdata.write(self.game.high_score_names[i] + " " + \
                    str(self.game.high_scores[i]) + "\n")
    
    def space_press(self):
        """handles pressing space key"""
        if self.menu_option == START:
            self.game.done = True
            self.state_stack.append(states.cut.Cut())
        elif self.menu_option == INSTRUCT:
            self.game.done = True
            self.state_stack.append(states.instructions.Instruct())
        elif self.menu_option == SCORE:
            self.game.done = True
            self.state_stack.append(states.highscore.High())
        elif self.menu_option == QUIT:
            self.game.done = True
    
    def down_press(self):
        """handles presssing down key"""
        if self.menu_option < 3:
            self.menu_option += 1
        else:
            self.menu_option = 0
    
    def up_press(self):
        """handles pressing up key"""
        if self.menu_option > 0:
            self.menu_option -= 1
        else:
            self.menu_option = 3

    def highlight(self):
        """colors currently selected menu item"""
        for current_item in self.menu_items:
            current_item.rgb = RGB_UNSELECTED
        self.menu_items[self.menu_option].rgb = RGB_SELECTED
