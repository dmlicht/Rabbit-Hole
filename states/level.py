"""
Handles gameplay in levels
"""

from __future__ import division
import pygame
import rabbyt
import tiles
import player
import healthbar
import chronos
import wave_handler
from settings import FontSprite
import states.menu
import states.highscore
import random
import actions
import copy
import movement_pattern
import sys
import os

SCREEN_HEIGHT   = 600
SCREEN_WIDTH    = 800

MAX_FUEL        = 100.0
FUEL_DRAIN      = 10.0
MIN_FUEL        = 0	
FUEL_REGAIN     = .1

TIME_TRAVEL_CHRONOS_DRAIN = .5
STARTING_CHRONOS = 100

class Level():
    """level class"""
    def __init__(self, game, level, state_after=""):
        self.wave_builder = wave_handler.WaveHandler(level)
        self.wave_builder.parse_level_file()
        self.set_scheduler_waves()
        self.set_up_music()

        game.set_state_time()
        self.background             = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, \
                                    self.wave_builder.layout_file_path, game)


        self.state_stack            = game.game_states
        self.game                   = game

        self.state_after            = state_after

        self.joystick               = 0

        self.energy                 = STARTING_CHRONOS
        self.fuel                   = MAX_FUEL

        #player
        self.ship                   = player.User("3ship1", game.screen)
        self.past_selves            = []
        self.f_xy                   = []   

        self.bullets                = []
        self.enemies                = []
        self.enemy_bullets          = []
        self.items                  = []

        self.stored_enemies         = []
        self.stored_bullets         = []
        self.stored_enemy_bullets   = []
        self.stored_items           = []
        self.stored_past_selves     = []

        #set UI
        self.text_score         = FontSprite(game.font, "Score: " + \
                                  str(self.game.user.score))
        self.text_score.rgb     = (255, 255, 255)
        self.text_score.xy      = (-380, -260)
        self.text_boost         = FontSprite(game.font, "Boost Fuel: " + \
                                  str(self.fuel))
        self.text_boost.rgb     = (160, 160, 160)
        self.text_boost.xy      = (-380, -240)
        self.text_health        = FontSprite(game.font, "Health: " + \
                                  str(self.ship.health))
        self.text_health.rgb    = (255, 255, 255)
        self.text_health.xy     = (200, -240)
        self.text_chronos       = FontSprite(game.font, "Chronos: " + \
                                  str(self.energy))
        self.text_chronos.rgb   = (255, 255, 255)
        self.text_chronos.xy    = (200, -260)

        #health bar
        self.healthbar          = healthbar.HealthBar()
    
        self.masks = []

        #finished?
        self.done               = False
        self.boss_dead          = False

        self.saving             = False
        self.can_store          = True
        self.stored_offset      = 0
        self.current_offset     = 0

        self.travel_toggle      = False
        self.let_go_of_travel   = True
    

        if self.wave_builder.mask_file_path:
            self.masks.append(rabbyt.Sprite(self.wave_builder.mask_file_path))
            self.masks[0].x = rabbyt.lerp(400, -400, dt=1, extend="reverse")

    def set_up_music(self):
        song = self.wave_builder.music_file_path
        print song
        if song and os.path.exists(song):
            print song, " exists"
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(-1, 0.0)
    
    def run(self, game, state_stack):
        """runs the game"""
        rabbyt.set_time(self.get_ticks()/1000.0)
        self.done = False
        self.game = game
        #rabbyt.scheduler.add((game.get_ticks() + \ 
        #self.background.row_update_time)/1000, self.update_tiles_loop)

        self.background.initialize()

        while not self.done:
            self.continue_level()
            all_enemies_defeated = (self.wave_builder.all_waves_called() and \
            len(self.enemies) == 0)
            if all_enemies_defeated or self.boss_dead:
                self.victory_end()
            if self.ship.health <= 0:
                self.failure_end()
            
    def continue_level(self):
        """continues"""
        if self.game.get_ticks() - self.game.fps > 1000:
            print "FPS: ", self.game.clock.get_fps()
            self.game.fps = self.game.get_ticks()

        self.handle_user_events()

        if self.saving:
            self.handle_save()
        #Timing
        rabbyt.set_time(self.get_ticks()/1000.0)
        rabbyt.scheduler.pump()
        rabbyt.clear()

        #Update
        self.update_UI()
        self.update_game_objects()
        self.handle_collisions_between(self.ship, self.enemies)
        self.handle_collisions_between(self.ship, self.enemy_bullets)
        self.handle_collisions_between(self.bullets, self.enemies)
        self.handle_collisions_between(self.past_selves, self.enemies)
        self.handle_collisions_between(self.past_selves, self.enemy_bullets)
        self.handle_item_pickups_between(self.ship, self.items)

        #Render
        self.render_game_objects()

        self.game.clock.tick(40)
        pygame.display.flip()

    def handle_user_events(self):
        """handles input"""
        #check for quitting
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                self.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(self.game.high_score_names[i] + " " + \
                                str(self.game.high_scores[i]) + "\n")
            elif event.type == pygame.KEYDOWN:
                self.joystick = 0
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_n:
                    self.done = True
                    self.state_stack.append(self.state_after)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.joystick = 1
                if self.game.joystick.get_button(self.game.controls.settings["Escape"]):
                    self.done = True
                    self.state_stack.append(states.menu.Menu())
                elif self.game.joystick.get_button(self.game.controls.settings["Skip"]):
                    self.done = True
                    self.state_stack.append(self.state_after)
            #elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                #self.ship.has_fired = False
        
        #check for key pressed
        user_actions = actions.Actions()
        if self.joystick:
            user_actions = self.joystick_to_actions()
            self.ship.handle_actions(user_actions, self)
        else:
            pressed = pygame.key.get_pressed()
            user_actions = self.keyboard_to_actions(pressed)
            self.ship.handle_actions(user_actions, self)

        #save ship movements
        if user_actions.toggle_time_travel:
            if self.let_go_of_travel:
                self.get_set_travel()
            self.let_go_of_travel = False
        else:
            self.let_go_of_travel = True

        if self.saving:
            self.ship.save_actions(self.get_ticks(), user_actions)

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
        if pressed[pygame.K_c]: user_actions.toggle_time_travel = True
        return user_actions

    def joystick_to_actions(self):
        user_actions = actions.Actions()
        joy = self.game.joystick
        #print joy 4, 6, 7, 10
        if joy.get_button(self.game.controls.settings["Up"]): user_actions.up = True
        if joy.get_button(self.game.controls.settings["Down"]): user_actions.down = True
        if joy.get_button(self.game.controls.settings["Left"]):  user_actions.left = True
        if joy.get_button(self.game.controls.settings["Right"]): user_actions.right = True
        if joy.get_button(self.game.controls.settings["Fire"]): user_actions.fire = True
        if joy.get_button(self.game.controls.settings["Boost"]): user_actions.boost = True
        if joy.get_button(self.game.controls.settings["Tilt left"]): user_actions.tilt_left = True
        if joy.get_button(self.game.controls.settings["Tilt right"]): user_actions.tilt_right = True
        if joy.get_button(self.game.controls.settings["Toggle time travel"]): 
            print "true" 
            user_actions.toggle_time_travel = True
        return user_actions


    def get_set_travel(self):
        if self.travel_toggle == False and self.can_store:
            self.set_travel_point()
        else:
            self.return_travel_point()

    def update_UI(self):
        """updates UI"""
        self.text_health.text = "Health: " + str(self.ship.health)
        self.text_score.text = "Score: " + str(self.game.user.score)
        self.text_boost.text = "Boost Fuel: " + str(self.ship.boost_fuel)

    def update_game_objects(self):
        """updates objects"""
        self.background.maintain_tile_rows()
        self.ship.update()
        self.remove_offmap(self.bullets)
        self.handle_enemy_fire()

        #for gem in self.sparks:
        #    gem.update()
        for enemy in self.enemies:
            enemy.animate()

        for past_self in self.past_selves:
            if not past_self.get_actions(self.get_ticks()):
                self.past_selves.remove(past_self)
            else: past_self.update()

                
        self.remove_offmap(self.enemies)
        self.remove_offmap(self.items)

    def handle_enemy_fire(self):
        for enemy in self.enemies:
            enemy_bullet = enemy.fire(self)

    def render_game_objects(self):
        """rabbyt render methods"""
        self.background.render()
        rabbyt.render_unsorted(self.masks)
        self.ship.render()

        rabbyt.render_unsorted(self.bullets)
        rabbyt.render_unsorted(self.enemies)
        rabbyt.render_unsorted(self.items)
        rabbyt.render_unsorted(self.past_selves)
        rabbyt.render_unsorted(self.enemy_bullets)


        self.text_score.render()
        self.text_boost.render()
        self.text_health.render()
        self.text_chronos.render()

        self.healthbar.render()

    def remove_offmap(self, objects_to_check):
        """removes if offmap"""
        for current in objects_to_check:
            if current.isOffMap():
                objects_to_check.remove(current)

    def handle_collisions_between(self, set1, set2):
        """handling collisions"""
        set_one_is_list = isinstance(set1, list)
        set_two_is_list = isinstance(set2, list)

        if set_one_is_list and set_two_is_list:
            self.check_collisions_using(rabbyt.collisions.collide_groups, \
                                        set1, set2)

        elif set_two_is_list:
            collision_occured = self.check_collisions_using( \
                                rabbyt.collisions.collide_single, set1, set2)
            if collision_occured: 
                var = set1.hit()
                print set1.__class__.__name__
                print var
	        if set1.__class__.__name__ == "User" and var:
                   self.healthbar.hit()    

        elif set_one_is_list:
            collision_occured = self.check_collisions_using( \
                                rabbyt.collisions.collide_single, set2, set1)
            if collision_occured: 
                set2.hit()

        else: #wrap both singular objects into sets and then test
            set1wrapper = []
            set1wrapper.append(set1)

            set2wrapper = []
            set2wrapper.append(set2)

            self.check_collisions_using(rabbyt.collisions.collide_groups, \
                                        set1wrapper, set2wrapper)

    def check_collisions_using(self, collision_function, set1, set2):
        """returns true if there are collisions"""
        collisions = collision_function(set1, set2)
        if len(collisions) and isinstance(collisions[0], tuple): 
            for objects_that_were_hit in collisions:

                objects_that_were_hit[0].hit()
                #to add damage uncomment line below and comment out line above
                #objects_that_were_hit[0].hit(objects_that_were_hit[1].damage)
                if objects_that_were_hit[0].health <= 0:
                    self.game.user.score += objects_that_were_hit[0].die(self)
                    if set1.count(objects_that_were_hit[0]) > 0:
                        set1.remove(objects_that_were_hit[0])

                objects_that_were_hit[1].hit()
                xy = objects_that_were_hit[1].xy

                #to add damage uncomment line below and comment out line above
                #objects_that_were_hit[1].hit(objects_that_were_hit[0].damage)
                if objects_that_were_hit[1].health <= 0:
                    self.game.user.score += objects_that_were_hit[1].die(self)
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

    def handle_item_pickups_between(self, ship, items):
        touched_items = rabbyt.collisions.collide_single(ship, items)
        for item in touched_items:
            if item in self.items:
                self.items.remove(item)
                self.energy += 100
                self.game.gem_pickup_sound.play()
                self.text_chronos.text = "Chronos: " + str(self.energy)

    def set_scheduler_waves(self):
        """set scheduler for waves"""
        for time in self.wave_builder.get_wave_times():
            print time
            rabbyt.scheduler.add(time, self.build_wave)

    def build_wave(self):
        """build waves"""
        current_wave = self.wave_builder.get_next_wave()
        if current_wave:
            for element in current_wave.elements:
                new_enemy = element.enemy_type(self.game.screen, element.startx,
                element.starty, element.patternx, element.patterny)
                self.enemies.append(new_enemy)

    def handle_save(self):
        self.energy -= TIME_TRAVEL_CHRONOS_DRAIN
        self.text_chronos.text = "Chronos: " + str(self.energy)
        if self.energy <= 0:
            self.return_travel_point()

    def victory_end(self):
        """yay we win"""
        if isinstance(self.state_after, states.highscore.High):
            self.game.update_scores()
        self.state_stack.append(self.state_after)
        pygame.mixer.music.stop()
        self.done = True

    def failure_end(self):
        """uh oh"""
        self.game.update_scores()
        self.state_stack.append(states.highscore.High())
        pygame.mixer.music.stop()
        self.game.lose_sound.play()
        self.done = True
    
    def get_ticks(self):
        return self.game.get_ticks() - self.current_offset

    def set_travel_point(self):
        self.saving = True
        self.background.saving = True
        self.stored_offset = self.get_ticks()
        self.ship.save()
        self.save_enemies()
        self.save_bullets()
        self.save_enemy_bullets()
        self.save_items()
        self.save_past_selves()
        self.can_store = False

    def save_enemies(self):
        self.stored_enemies = []
        for enemy in self.enemies:
            self.stored_enemies.append(enemy)

    def save_bullets(self):
        self.stored_bullets = []
        for bullet in self.bullets:
            self.stored_bullets.append(bullet)

    def save_enemy_bullets(self):
        self.stored_enemy_bullets = []
        for enemy_bullet in self.enemy_bullets:
            self.stored_enemy_bullets.append(enemy_bullet)

    def save_items(self):
        self.stored_items = []
        for item in self.items:
            self.stored_items.append(item)

    def save_past_selves(self):
        self.stored_past_selves = []
        for past_self in self.past_selves:
            self.stored_past_selves.append(past_self)

    def return_travel_point(self):
        self.saving = False
        self.background.saving = False
        self.readd_waves()
        self.current_offset = self.game.get_ticks() - self.stored_offset
        new_past_self = player.PastSelf("3ship1", self.game.screen, self.ship.saved_xy, \
                        self.ship.saved_rot, self.ship.saved_actions, self)
        self.can_store = True
        self.ship.saved_actions = []
        self.return_past_selves()
        self.past_selves.append(new_past_self)
        self.return_bullets()
        self.return_enemy_bullets()
        self.return_enemies()
        self.return_items()
        self.time_travel_animation()

    def readd_waves(self):
        for time in self.wave_builder.readd_waves(self.stored_offset, self.get_ticks()):
            print time
            rabbyt.scheduler.add(time, self.build_wave)

    def return_bullets(self):
        self.bullets = self.stored_bullets
        self.stored_bullets = []

    def return_enemy_bullets(self):
        self.enemy_bullets = self.stored_enemy_bullets
        self.stored_enemy_bullets = []
        
    def return_enemies(self):
        self.enemies = self.stored_enemies
        self.stored_enemies = []

    def return_items(self):
        self.items = self.stored_items
        self.stored_items = []
    
    def return_past_selves(self):
        self.past_selves = self.stored_past_selves
    
    def time_travel_animation(self):
        warp_speed = 20
        while self.ship.y < 500:
            self.ship.y += warp_speed
            self.ship.render()
            pygame.display.flip()
        self.ship.xy = self.ship.saved_xy
        saved_y = self.ship.y
        self.ship.y = -500
        self.background.render()
        rabbyt.render_unsorted(self.masks)
        while self.ship.y < saved_y - 100:
            self.ship.y += 1
            self.ship.render()
            pygame.display.flip()

