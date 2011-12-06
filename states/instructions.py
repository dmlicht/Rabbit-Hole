"""
Instruction State
"""
from __future__ import division
import pygame
import rabbyt

import state
import states.menu
from settings import FontSprite

import actions
import player
import bullet

class Instruct(state.State):
    """Instruct State"""
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.ship = player.Ship("3ship1", self.screen)
        self.ship.xy = (0, 80)

        self.bullets = []

        self.joystick = 0

    def run(self, game, state_stack):
        backg = rabbyt.Sprite('1Menu_Screen1.png') 
        arrows = rabbyt.Sprite('1arrows.png') 
        tilt = rabbyt.Sprite('1zx.png') 
        time = rabbyt.Sprite('1c.png') 
        space = rabbyt.Sprite('1sp.png') 
        dash = rabbyt.Sprite('1d.png') 
        arrows.xy = (-295, 80)
        tilt.xy = (-295, -36)
        time.xy = (-295, -109)
        space.xy = (-295, -183)
        dash.xy = (-295, -257)

        game.done = False
        while not game.done:
            rabbyt.set_time(game.get_ticks()/1000.0)
            rabbyt.scheduler.pump()
            rabbyt.clear()
            for event in pygame.event.get():
                if event.type ==  pygame.QUIT:
                    game.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(game.high_score_names[i] + " " + \
                        str(game.high_scores[i]) + "\n")
                elif event.type == pygame.KEYDOWN:
                    self.joystick = 0
                    if event.key == pygame.K_ESCAPE:
                        game.done = True
                        state_stack.append(states.menu.Menu())
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.joystick = 1
                    if game.joystick.get_button(game.controls.settings["Escape"]):
                        game.done = True
                        state_stack.append(states.menu.Menu())

            backg.render()
            arrows.render()
            tilt.render()
            time.render()
            space.render()
            dash.render()
            rabbyt.render_unsorted(self.bullets)

            if self.joystick:
                user_actions = self.joystick_to_actions(game)
                self.ship.handle_actions(user_actions, self)
            else:
                pressed = pygame.key.get_pressed()
                user_actions = self.keyboard_to_actions(pressed)
                self.ship.handle_actions(user_actions, self)
                
            for bullet in self.bullets:
                if bullet.isOffMap():
                    self.bullets.remove(bullet)

            self.ship.update()
            self.ship.render()

            game.clock.tick(40)
            pygame.display.flip()

    def keyboard_to_actions(self, pressed):
        user_actions = actions.Actions()
        if pressed[pygame.K_UP]: user_actions.up = True
        if pressed[pygame.K_DOWN]: user_actions.down = True
        if pressed[pygame.K_LEFT]:  user_actions.left = True
        if pressed[pygame.K_RIGHT]: user_actions.right = True
        if pressed[pygame.K_SPACE]: user_actions.fire = True
        if pressed[pygame.K_d]: user_actions.boost = True
        if pressed[pygame.K_z]: user_actions.tilt_left = True
        if pressed[pygame.K_x]: user_actions.tilt_right = True
        return user_actions

    def joystick_to_actions(self, game):
        user_actions = actions.Actions()
        joy = game.joystick
        #print joy 4, 6, 7, 10
        if joy.get_button(game.controls.settings["Up"]): user_actions.up = True
        if joy.get_button(game.controls.settings["Down"]): user_actions.down = True
        if joy.get_button(game.controls.settings["Left"]):  user_actions.left = True
        if joy.get_button(game.controls.settings["Right"]): user_actions.right = True
        if joy.get_button(game.controls.settings["Fire"]): user_actions.fire = True
        if joy.get_button(game.controls.settings["Boost"]): user_actions.boost = True
        if joy.get_button(game.controls.settings["Tilt left"]): user_actions.tilt_left = True
        if joy.get_button(game.controls.settings["Tilt right"]): user_actions.tilt_right = True
        if joy.get_button(game.controls.settings["Toggle time travel"]): 
            print "true" 
            user_actions.toggle_time_travel = True
        return user_actions
