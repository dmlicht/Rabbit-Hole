from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands
import wave, wave_element, wave_handler
from settings import Font, FontSprite
import state, states.menu

SCREEN_HEIGHT   = 600
SCREEN_WIDTH    = 800

MAX_FUEL        = 100.0
FUEL_DRAIN      = 10.0
MIN_FUEL        = 0	
FUEL_REGAIN     = .1

class Level():
    def __init__(self, game, level, state_after=""):
        self.wave_builder = wave_handler.WaveHandler(level)
        self.wave_builder.parse_level_file()
        self.set_scheduler_waves()

        self.background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, self.wave_builder.layout_file_path)
        self.background.initialize()

        self.state_stack = game.game_states
        self.game = game

        self.state_after        = state_after

        self.energy             = 100
        self.fuel               = MAX_FUEL

        #player
        self.ship               = player.Ship("3ship1", game.screen)
        self.f_xy               = []   
        self.bullets            = []
        self.enemies            = []

        #set UI
        self.text_score         = FontSprite(game.font, "Score: " + str(self.game.user.score))
        self.text_score.rgb     = (255,255,255)
        self.text_score.xy      = (-380, -260)
        self.text_boost         = FontSprite(game.font, "Boost Fuel: " + str(self.fuel))
        self.text_boost.rgb     = (160,160,160)
        self.text_boost.xy      = (-380, -240)
        self.text_health        = FontSprite(game.font, "Health: " + str(self.ship.health))
        self.text_health.rgb    = (255,255,255)
        self.text_health.xy     = (200, -240)
        self.text_chronos       = FontSprite(game.font, "Chronos: " + str(self.energy))
        self.text_chronos.rgb   = (255,255,255)
        self.text_chronos.xy    = (200, -260)

        #health bar
        self.bar                = rabbyt.Sprite(0, (0,20,200,0))
        self.bar.rgb            = (34,139,34)
        self.bar.xy             = (200, -240)

        self.back_time          = 0
    
    def run(self, game, state_stack):
        self.done = False
        self.game = game

        while not self.done:
            self.continue_level()
            all_enemies_defeated = (self.wave_builder.all_waves_called() and len(self.enemies) == 0)
            if all_enemies_defeated:
                self.victory_end()
            
    def continue_level(self):
            if pygame.time.get_ticks() - self.game.fps > 1000:
                print "FPS: ", self.game.clock.get_fps()
                self.game.fps = pygame.time.get_ticks()

            self.handle_user_events()

            #Timing
            rabbyt.set_time(pygame.time.get_ticks()/1000.0 + self.back_time)
            rabbyt.scheduler.pump()
            rabbyt.clear()

            #Update
            self.update_UI()
            self.update_game_objects()
            self.handle_collisions_between(self.ship, self.enemies)
            self.handle_collisions_between(self.bullets, self.enemies)

            #Render
            self.render_game_objects()

            self.game.clock.tick(40)
            pygame.display.flip()

    def handle_user_events(self):

            #check for quitting
            for event in pygame.event.get():
                if event.type ==  QUIT:
                    self.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(self.game.highScoreNames[i] + " " + str(self.game.highScores[i]) + "\n")
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                        self.state_stack.append(states.menu.Menu())
                elif event.type == KEYUP and event.key == K_SPACE:
                    self.ship.has_fired= False    
            pressed = pygame.key.get_pressed()

            #ship boost
            if pressed[K_d]:
                self.ship.boosting = True
            else: self.ship.boosting = False
            self.text_boost.text = "Boost Fuel: " + str(self.ship.boost_fuel)

	        #ship animation
            if pressed[K_UP] != 0 or pressed[K_DOWN] != 0 or pressed[K_LEFT] != 0 or pressed[K_RIGHT] != 0:
                self.ship.animate()

	        #Vertical Movement
            self.ship.acceleration_y = pressed[K_UP] - pressed[K_DOWN]
            self.ship.check_vertical_bounds()

	        #Horizontal Movement
            self.ship.acceleration_x = pressed[K_RIGHT] - pressed[K_LEFT]
            self.ship.check_horizontal_bounds()

            #Firing
            if pressed[K_SPACE]:
                new_bullet = self.ship.attemptfire()
                if new_bullet:
                    self.bullets.append(new_bullet)
            #tilt
            self.ship.tilt = pressed[K_z] - pressed[K_x]

    def update_UI(self):
            self.text_health.text = "Health: " + str(self.ship.health)
            self.text_score.text = "Score: " + str(self.game.user.score)
            if self.fuel < MAX_FUEL:
                self.fuel += FUEL_REGAIN
                self.text_boost.text = "Boost Fuel: " + str(self.fuel)
            else:
                self.fuel = 100.0
                self.text_boost.text = "Boost Fuel: " + str(self.fuel)

    def update_game_objects(self):
            self.background.maintain_tile_rows()
            self.ship.update()
            self.remove_offmap(self.bullets)
            self.remove_offmap(self.enemies)

            for enemy in self.enemies:
                enemy.animate()

    def render_game_objects(self):
            self.background.render()
            self.ship.render()

            rabbyt.render_unsorted(self.bullets)
            rabbyt.render_unsorted(self.enemies)

            self.text_score.render()
            self.text_boost.render()
            self.text_health.render()
            self.text_chronos.render()

	    self.bar.render()

    def remove_offmap(self, objects_to_check):
        for current in objects_to_check:
            if current.isOffMap():
                objects_to_check.remove(current)

    def handle_collisions_between(self, set1, set2):

        set_one_is_list = isinstance(set1, list)
        set_two_is_list = isinstance(set2, list)

        if set_one_is_list and set_two_is_list:
            self.check_collisions_using(rabbyt.collisions.collide_groups, set1, set2)
            self.check_collisions_using(rabbyt.collisions.collide_groups, set2, set1)

        elif set_two_is_list:
            collision_occured = self.check_collisions_using(rabbyt.collisions.collide_single, set1, set2)
            if collision_occured: 
		set1.hit()
		if self.bar.shape[2][0] > 0:
                    temp = self.bar.shape
                    self.bar.shape = (0,temp[1][1],temp[2][0]-20,0)
	    

        elif set_one_is_list:
            collision_occured = self.check_collisions_using(rabbyt.collisions.collide_single, set2, set1)
            if collision_occured: set2.hit()

        else: #wrap both singular objects into sets and then test
            set1wrapper = []
            set1wrapper.append(set1)

            set2wrapper = []
            set2wrapper.append(set2)

            self.check_collisions_using(rabbyt.collisions.collide_groups, set1wrapper, set2wrapper)

    #returns true if there are collisions.
    def check_collisions_using(self, collision_function, set1, set2):
        collisions = collision_function(set1, set2)
        if len(collisions) and isinstance(collisions[0], tuple): #check if groups collided
            for objects_that_were_hit in collisions:

                objects_that_were_hit[0].hit()
                #to incorperate damage uncomment line below and comment out line above
                #objects_that_were_hit[0].hit(objects_that_were_hit[1].damage)
                if objects_that_were_hit[0].health <= 0:
                    self.game.user.score += objects_that_were_hit[0].die()
                    set1.remove(objects_that_were_hit[0])

                objects_that_were_hit[1].hit()
                #to incorperate damage uncomment line below and comment out line above
                #objects_that_were_hit[1].hit(objects_that_were_hit[0].damage)
                if objects_that_were_hit[1].health <= 0:
                    self.game.user.score += objects_that_were_hit[1].die()
                    set2.remove(objects_that_were_hit[1])

        else:
            for object_that_was_hit in collisions:
                object_that_was_hit.hit()
                if not object_that_was_hit.health > 0:
                    set2.remove(object_that_was_hit)
        if collisions:
            return True
        else:
            return False

    def set_scheduler_waves(self):
        for time in self.wave_builder.get_wave_times():
            print time
            rabbyt.scheduler.add(time, self.build_wave)

    def build_wave(self):
        current_wave = self.wave_builder.get_next_wave()
        if current_wave:
            for element in current_wave.elements:
                new_enemy = element.enemy_type(self.game.screen, element.startx, element.starty, element.patternx, element.patterny)
                self.enemies.append(new_enemy)

    def victory_end(self):
        self.state_stack.append(self.state_after)
        self.done = True

    def failure_end(self):
        self.done = True
