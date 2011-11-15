"""
Handles ALL the levels
"""

from __future__ import division
import pygame, rabbyt
import tiles
import player, healthbar
import wave_handler
from settings import FontSprite
import states.menu, states.highscore
SCREEN_HEIGHT   = 600
SCREEN_WIDTH    = 800

MAX_FUEL        = 100.0
FUEL_DRAIN      = 10.0
MIN_FUEL        = 0	
FUEL_REGAIN     = .1

class Level():
    """level class"""
    def __init__(self, game, level, state_after=""):
        self.wave_builder = wave_handler.WaveHandler(level)
        self.wave_builder.parse_level_file()
        self.set_scheduler_waves()

        game.set_state_time()
        self.background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, \
                          self.wave_builder.layout_file_path, game)
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
        self.healthbar                = healthbar.HealthBar()

        #finished?
        self.done = False
    
    def run(self, game, state_stack):
        """runs the game"""
        rabbyt.set_time(self.game.get_ticks()/1000.0)
        self.done = False
        self.game = game
        #rabbyt.scheduler.add((game.get_ticks() + \ 
        #self.background.row_update_time)/1000, self.update_tiles_loop)

        while not self.done:
            self.continue_level()
            all_enemies_defeated = (self.wave_builder.all_waves_called() and \
            len(self.enemies) == 0)
            if all_enemies_defeated:
                self.victory_end()
            if self.ship.health <= 0:
                self.failure_end()
            
    def continue_level(self):
        """continues"""
        if self.game.get_ticks() - self.game.fps > 1000:
            print "FPS: ", self.game.clock.get_fps()
            self.game.fps = self.game.get_ticks()

        self.handle_user_events()

        #Timing
        rabbyt.set_time(self.game.get_ticks()/1000.0)
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
        """handles input"""
        #check for quitting
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                self.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(self.game.highScoreNames[i] + " " + \
                                str(self.game.highScores[i]) + "\n")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                    self.state_stack.append(states.menu.Menu())
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.ship.has_fired = False    
        pressed = pygame.key.get_pressed()

        #ship boost
        if pressed[pygame.K_d]:
            self.ship.boosting = True
        else: self.ship.boosting = False
        self.text_boost.text = "Boost Fuel: " + str(self.ship.boost_fuel)

        #ship animation
        if pressed[pygame.K_UP] != 0 or pressed[pygame.K_DOWN] != 0 or \
        pressed[pygame.K_LEFT] != 0 or pressed[pygame.K_RIGHT] != 0:
            self.ship.animate()

        #Vertical Movement
        self.ship.acceleration_y = pressed[pygame.K_UP] - pressed[pygame.K_DOWN]
        self.ship.check_vertical_bounds()
        #Horizontal Movement
        self.ship.acceleration_x = pressed[pygame.K_RIGHT] - \
                                   pressed[pygame.K_LEFT]
        self.ship.check_horizontal_bounds()

        #Firing
        if pressed[pygame.K_SPACE]:
            new_bullet = self.ship.attemptfire()
            if new_bullet:
                self.bullets.append(new_bullet)
        #tilt
        self.ship.tilt = pressed[pygame.K_z] - pressed[pygame.K_x]

    def update_UI(self):
        """updates UI"""
        self.text_health.text = "Health: " + str(self.ship.health)
        self.text_score.text = "Score: " + str(self.game.user.score)
        if self.fuel < MAX_FUEL:
            self.fuel += FUEL_REGAIN
            self.text_boost.text = "Boost Fuel: " + str(self.fuel)
        else:
            self.fuel = 100.0
            self.text_boost.text = "Boost Fuel: " + str(self.fuel)

    def update_game_objects(self):
        """updates objects"""
        self.background.maintain_tile_rows()
        self.ship.update()
        self.remove_offmap(self.bullets)

        for enemy in self.enemies:
            enemy.animate()
            """if enemy.checkBounds():
                self.game.user.score += 25"""
                
        self.remove_offmap(self.enemies)

    def render_game_objects(self):
        """rabbyt render methods"""
        self.background.render()
        self.ship.render()

        rabbyt.render_unsorted(self.bullets)
        rabbyt.render_unsorted(self.enemies)

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
                set1.hit()
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
                    self.game.user.score += objects_that_were_hit[0].die()
                    if set1.count(objects_that_were_hit[0]) > 0:
                        set1.remove(objects_that_were_hit[0])

                objects_that_were_hit[1].hit()
                #to add damage uncomment line below and comment out line above
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

    def victory_end(self):
        """yay we win"""
        if isinstance(self.state_after, states.highscore.High):
            self.game.update_scores()
        self.state_stack.append(self.state_after)
        self.done = True

    def failure_end(self):
        """uh oh"""
        self.game.update_scores()
        self.state_stack.append(states.highscore.High())
        self.done = True

    """
    def update_tiles_loop(self):
        print 'called update_tiles_loop'
        self.background.maintain_tile_rows()
        rabbyt.scheduler.add((self.game.get_ticks() + self.background.row_update_time)/1000.0, self.update_tiles_loop)
    """
