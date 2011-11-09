from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands
from settings import Font, FontSprite

BACKGROUND_SCROLL_TIME = 4
TILE_HEIGHT = 100
TILE_WIDTH = 100
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

def PlayScreen(self, state_stack):

    self.bGod = False
    self.bHaveFired = False
    self.bEnemy = True
    self.bFreeze = False
    self.numEnemies = 10
    self.dashable = True
    self.score = 0
    self.boss_out = False
    self.cooldown = 100
    self.bSaved = False

    self.past_events = []
    self.past_enemies = []
    self.past_player = []

    self.level = 1
    self.hero_dirx = -1
    self.hero_diry = -1

    self.ret_count = 0
    self.boss_count = 0
    self.energy = 100
    self.health = 3

    self.enTimer = pygame.time.Clock()
    self.enT = 0
    self.oldT = 0
    self.bossTimer = pygame.time.Clock()
    self.bossT = 0
    self.oldbT = 0
    clock = pygame.time.Clock() 
    self.invincibility_timer = pygame.time.Clock() 
    self.invincible = 0

    MAX_FUEL = 100.0
    FUEL_DRAIN = 10.0
    MIN_FUEL = 0	
    FUEL_REGAIN = .1
    self.fuel = MAX_FUEL
        
    text_score = FontSprite(self.font, "Score: " + str(self.score))
    text_score.rgb = (255,255,255)
    text_score.xy = (-380, -260)
    text_boost = FontSprite(self.font, "Boost Fuel: " + str(self.fuel))
    text_boost.rgb = (160,160,160)
    text_boost.xy = (-380, -240)
    text_health = FontSprite(self.font, "Health: " + str(self.health))
    text_health.rgb = (255,255,255)
    text_health.xy = (234, -260)
    text_chronos = FontSprite(self.font, "Chronos: " + str(self.energy))
    text_chronos.rgb = (255,255,255)
    text_chronos.xy = (234, -240)
    
    lev1time = 2500
    lev2time = 1750
    lev1atpatterns = [0, 0, 1, 1, 0, 1, 3]
    lev1movpatterns = [0, 2, 1, 2, 0, 1, 2]
    lev1bpatterns = [0, 1, 2, 1, 0, 1, 2]
    lev2atpatterns = [0, 0, 0, 1, 3, 1, 2, 2, 1, 3]
    lev2bpatterns = [0, 0, 1, 0, 1, 0, 1, 0, 0, 2]
    lev2movpatterns = [0, 1, 2, 0, 1, 2, 0, 1, 2, 1]
    pat_num = 0
    pat_num_b = 0
    self.h1_count = 0
    self.h2_count = 0
    #players
    self.ship = player.Ship("3ship1", self.screen)

    self.dragons = []
    for i in range(10):
        dragon = enemy.Dragon("7dragon", self.screen, 3, 0, (i*800.0/10 - 400)) #random.randint(0,2))
        self.dragons.append(dragon)

    self.bullets = []
    self.en_bullets = []
    sparks = []

    self.f_xy = []

    #background = rabbyt.Sprite("1deep-space.png")
    #BACKGROUNDS!
    background = tiles.Background(TILE_WIDTH, TILE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_SCROLL_TIME)
    background.initialize()

    self.done = False
    while not self.done:
        if pygame.time.get_ticks() - self.fps > 1000:
            print "FPS: ", self.clock.get_fps()
            self.fps = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type ==  QUIT:
                self.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(self.highScoreNames[i] + " " + str(self.highScores[i]) + "\n")
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.done = True
                    state_stack.append("Menu State")
            elif event.type == KEYUP and event.key == K_SPACE:
                self.bHaveFired = False    
            """elif event.type == KEYUP and event.key == K_r:
                if not self.bSaved:
                    self.past_player = python.copy.deep_copy(self.player)
                    for i in range(len(self.dragons)):
                        self.past_enemies[i] = python.copy.deep_copy(self.dragons[i])"""
        pressed = pygame.key.get_pressed()

            #ship boost
        if pressed[K_d]:
            self.ship.boosting = True
        else: self.ship.boosting = False
        text_boost.text = "Boost Fuel: " + str(self.ship.boost_fuel)
	        #self.fuel -= FUEL_DRAIN
          #      self.ship.boost()
	    #ship animation
        if pressed[K_UP] != 0 or pressed[K_DOWN] != 0 or pressed[K_LEFT] != 0 or pressed[K_RIGHT] != 0:
            self.ship.animate()
	    #Vertical Movement
        self.ship.acceleration_y = pressed[K_UP] - pressed[K_DOWN]
            #self.ship.accelerating = pressed[pygame.K_UP]
            #self.ship.backingup = pressed[pygame.K_DOWN]
        self.ship.check_vertical_bounds()
	    #Horizontal Movement
        self.ship.acceleration_x = pressed[K_RIGHT] - pressed[K_LEFT]
            #self.ship.turning_right = pressed[pygame.K_RIGHT]
            #self.ship.turning_left = pressed[pygame.K_LEFT]
        self.ship.check_horizontal_bounds()
            #ship godmode
        if pressed[K_BACKSPACE]:
            self.bGod = True
        if pressed[K_f] and self.energy > 0 and not self.bFreeze:
            self.bFreeze = True       
            for i in range(len(self.dragons)):
                self.f_xy.append(self.dragons[i].xy)
        elif pressed[K_f] and self.bFreeze:
            self.bFreeze = False
            for i in range(len(self.f_xy)):
                self.f_xy.pop()
        if self.bFreeze:
            self.energy -= 1
            text_chronos.text = "Chronos: " + str(self.energy)
            if self.energy <= 0:
                self.bFreeze = False
                for i in range(len(self.f_xy)):
                    self.f_xy.pop()
      #tilt
        self.ship.tilt = pressed[K_z] - pressed[K_x]
	    #ship firing
        if pressed[K_SPACE] and not self.bHaveFired:
            fired_bullet = bullet.Bullet(self.screen, self.ship.xy, self.ship.rot, 10)
            self.bullets.append(fired_bullet)
            self.bHaveFired = True

	    #adding enemies and looking for boss
        self.enT += self.enTimer.tick()
        if self.numEnemies >= 100 and not self.boss_out or pressed[pygame.K_b] and self.level == 1:
              self.boss0 = Boss0.Boss_zero(self.screen)
              self.boss_h1 = BossHands.Boss_hand('7dragon', self.screen, self.boss0, self.boss0.y, 75)
              self.boss_h2 = BossHands.Boss_hand('7dragon', self.screen, self.boss0, self.boss0.y, -75)
	      self.final = [self.boss0, self.boss_h1, self.boss_h2]
                #text_boss_health = FontSprite(self.font, "Boss: " + str(self.boss1.health))
                #text_boss_health.rgb = (255,255,255)
                #text_boss_health.xy = (100, 100)
              self.boss_out = True
              
        if self.numEnemies >= 200 and not self.boss_out or pressed[pygame.K_b] and self.level == 2:
              self.boss1 = Boss1.Boss(self.screen)
	      self.final = [self.boss1, self.ship]
                #text_boss_health = FontSprite(self.font, "Boss: " + str(self.boss1.health))
                #text_boss_health.rgb = (255,255,255)
                #text_boss_health.xy = (100, 100)
              self.boss_out = True
              
        if self.level == 1:
          if self.bEnemy and self.enT > self.oldT + lev1time and not self.numEnemies >= 100:
              self.oldT = self.enT
              self.bEnemy = False
              
        if self.level == 2:
          if self.bEnemy and self.enT > self.oldT + lev2time and not self.numEnemies >= 200:
              self.oldT = self.enT
              self.bEnemy = False

        if not self.bEnemy and not self.boss_out and not self.bFreeze and self.level == 1:
          self.bEnemy= True
          self.numEnemies += 5
          for i in range(5):
                if pat_num >= len(lev1atpatterns)-1:
                    pat_num = 0
                dragon = enemy.Dragon("7dragon", self.screen, lev1atpatterns[pat_num], lev1movpatterns[pat_num], (i*800.0/5 - 400)) #random.randint(0,2))
                    #dragon = enemy.Dragon("7dragon", self.screen, random.randint(0,2))
                self.dragons.append(dragon)
          pat_num += 1
            
        if not self.bEnemy and not self.boss_out and not self.bFreeze and self.level == 2:
            self.bEnemy= True
            self.numEnemies += 5
            for i in range(5):
                if pat_num >= len(lev2atpatterns)-1:
                    pat_num = 0
                dragon = enemy.Dragon("7dragon", self.screen, lev2atpatterns[pat_num], lev2movpatterns[pat_num], (i*800.0/5 - 400)) #random.randint(0,2))
                    #dragon = enemy.Dragon("7dragon", self.screen, random.randint(0,2))
                self.dragons.append(dragon)
            pat_num += 1
            #collisions
	    #dragon with ship
        self.invincible += self.invincibility_timer.tick()
        if self.invincible > 1000:
            for i in rabbyt.collisions.collide_single(self.ship, self.dragons):
                self.health -= 1
                text_health.text = "Health: " + str(self.health)
                self.invincible = 0

	    ##inserting names into highscore table
        if self.health <= 0 and not self.bGod:
            self.done = True
            state_stack.append("High Screen")
            self.lose_sound.play()

            self.score += (int)(self.energy/2)
            text_score.text = str(self.score)
            self.update_scores()
                  
            #bullet with enemies
        hits = rabbyt.collisions.collide_groups(self.bullets, self.dragons)
        for tup in hits:
            if tup[0] in self.bullets:
                xy = tup[1].xy
	        self.bullets.remove(tup[0])
                self.dragons.remove(tup[1])
	        self.score += 100
                text_score.text = "Score: " + str(self.score)

                    #spawning the chronium spark!
                t = random.randint(0, 10)
                if t == 0:
                    bob = chronos.Spark(self.screen, xy)
                    sparks.append(bob)
            #debug print self.bullets, self.dragons
  
            #chronos with player
        gems = rabbyt.collisions.collide_single(self.ship, sparks)
        for gem in gems:
            if gem in sparks:
                sparks.remove(gem)
                self.energy += 100
                self.gem_pickup_sound.play()
                text_chronos.text = "Chronos: " + str(self.energy)

	    #offmap
        for bull in self.bullets:
            if bull.checkBounds():
                self.bullets.remove(bull)
        for dragon in self.dragons:
            if dragon.checkBounds(): 
                self.dragons.remove(dragon)

        rabbyt.set_time(pygame.time.get_ticks()/1000.0)
        rabbyt.scheduler.pump()
        rabbyt.clear()

        #background handling
        background.maintain_tile_rows()
        background.render()
        #for row in background_tiles:
        #    rabbyt.render_unsorted(row)

	    #holy mackerel .. the boss ..
        if self.boss_out:
	        #text_boss_health.render()
            if self.level == 1:
              self.boss0.check_horizontal_bounds()
              #self.boss_h1.checkBounds()
              #self.boss_h2.checkBounds()
              self.boss0.render()
              self.boss_h1.render()
              self.boss_h2.render()
              self.bossT += self.bossTimer.tick()
              if self.bossT > self.oldbT+2500 and not self.bFreeze:
                if pat_num_b >= len(lev1bpatterns)-1:
                  pat_num_b = 0

                pat_num_b+=1  
                atp = lev1bpatterns[pat_num_b]
                if atp == 0:
                    self.h1_count = 1 
                elif atp == 1:
                    self.h2_count = 1
                else:
                    self.boss_count = 1
        
                self.oldbT = self.bossT    

              boss_hits = rabbyt.collisions.collide_single(self.boss0, self.bullets)
	      for boss_hit in boss_hits:
                if boss_hit in self.bullets:
                    self.bullets.remove(boss_hit)
                    remaining_health = self.boss0.lose_health(1)
	                #text_boss_health.text = "Boss Health:  " + str(self.boss1.health)
                    if remaining_health and self.level == 2:
                        self.done = True
                        state_stack.append("High Screen")
                        self.win_sound.play()
                        self.score += (int)(self.energy/2)+1000
	                text_score.text = "Score: " + str(self.score)
                        self.update_scores()
                    elif remaining_health and self.level == 1:
                        self.boss_out = False
                        pat_num = 0
                        pat_num_b = 0
                        self.boss_count = 0
                        self.score += 1000
                        self.level += 1
                        for i in range(len(self.dragons)):
                          self.dragons.pop()
                        for i in range(len(self.final)):
                          self.final.pop()  
                        self.numEnemies = 0
                        
              if self.boss_count > 0 and self.boss_count < 21:
                self.boss0.attack()
                self.boss_count += 1
              elif self.boss_count > 20:
                self.boss_count = 0
                self.ret_count = 1
              if self.h1_count > 0 and self.h1_count < 300:
                print 'calling hone_in on h1'
                self.boss_h1.hone_in(self.ship)
                self.h1_count += 1
              elif self.h1_count > 3000:
                self.h1_count = 0
              if self.h2_count > 0 and self.h2_count < 300:
                self.boss_h2.hone_in(self.ship)
                self.h2_count += 1
              elif self.h2_count > 3000:
                self.h2_count = 0

              if self.ret_count > 0 and self.ret_count < 21:
                 self.boss0.retreat()
                 self.ret_count += 1
              elif self.ret_count > 20:
                 self.ret_count = 0
                 
              player_hit = list(set(rabbyt.collisions.collide_single(self.ship, self.final)))
              self.health -= len(player_hit)
              if len(player_hit) > 0:
                  self.boss_count = 0
                  self.h1_count = 0
                  self.h2_count = 0
                  self.invincible = 500
              if self.health < 0:
                text_health.text = "Health: 0"         
              
              #if not self.bFreeze:
                #if self.boss_count == 0:
                    #self.boss0.update()
                #if self.h1_count == 0:
                    #self.boss_h1.hone_in(self.boss0.x-50, self.boss0.y)    
                #if self.h2_count == 0:
                    #self.boss_h2.hone_in(self.boss0.x+50, self.boss0.y)
              
                    
              self.boss0.render()
              self.boss_h1.render()
              self.boss_h2.render()
              
            if self.level == 2 and self.boss_out:
	      self.boss0.render()
              self.bossT += self.bossTimer.tick()
              if self.bossT > self.oldbT+1000 and not self.bFreeze:
                if pat_num_b >= len(lev2bpatterns)-1:
                    pat_num_b = 0
                atp = lev2bpatterns[pat_num_b]
                pat_num_b += 1 
                if atp == 0:
                    self.en_bu1 = bullet.Bullet(self.screen, self.boss1.xy, 225, 10)
                    self.en_bu2 = bullet.Bullet(self.screen, self.boss1.xy, 270, 10)
                    self.en_bu3 = bullet.Bullet(self.screen, self.boss1.xy, 315, 10)
                    self.en_bullets.append(self.en_bu1)
                    self.en_bullets.append(self.en_bu2)
                    self.en_bullets.append(self.en_bu3)
                elif atp == 1:
                    for i in range(3):
                        dragon = enemy.Dragon("7dragon", self.screen, 0,0)
                        self.dragons.append(dragon)
                else:
                    self.boss_count = 1
        
                self.oldbT = self.bossT    

              if self.boss_count > 0 and self.boss_count < 11:
                self.boss1.hone_in(self.ship.x, self.ship.y)
                self.boss_count += 1
              elif self.boss_count > 10:
                self.boss_count = 0

              boss_hits = rabbyt.collisions.collide_single(self.boss1, self.bullets)
	      for boss_hit in boss_hits:
                if boss_hit in self.bullets:
                    self.bullets.remove(boss_hit)
                    remaining_health = self.boss1.lose_health(1)
	                #text_boss_health.text = "Boss Health:  " + str(self.boss1.health)

                    if remaining_health and self.level == 2:
                        self.done = True
                        state_stack.append("High Screen")
                        self.win_sound.play()
                        self.score += (int)(self.energy/2)+1000
	                text_score.text = "Score: " + str(self.score)
                        self.update_scores()
                    elif remaining_health and self.level == 1:
                        self.boss_out = False
                        pat_num = 0
                        pat_num_b = 0
                        for i in range(len(self.dragons)):
                          self.dragons.pop()
                        self.numEnemies = 0
                        
              player_hit = list(set(rabbyt.collisions.collide(self.final)))
              if self.health - len(player_hit) < 0:
                text_health.text = "Health: 0"
                
              player_hit2 = list(set(rabbyt.collisions.collide_single(self.ship, self.en_bullets)))
              self.health -= len(player_hit2)
              if len(player_hit2) > 0:
                  self.invincible = 500

              for r in self.en_bullets:
                if r.checkBounds():
                    self.en_bullets.remove(r)        
              if not self.bFreeze:
                if self.boss_count == 0:
                    self.boss1.update()
                for bull in self.en_bullets:
                    bull.update()
 
              rabbyt.render_unsorted(self.en_bullets)
              self.boss1.render()                 

            if self.health <= 0 and self.bGod == False:
                self.done = True
                state_stack.append("High Screen")
                self.lose_sound.play()
                self.score += (int)(self.energy/2)
                self.score += self.energy*50+1000
                self.update_scores()

            

	    #updates
        self.ship.update()
	for b in self.bullets:
	    b.update()
	if self.bFreeze:
            for d in range(len(self.dragons)):
                self.dragons[d].freeze_Up(self.f_xy[d])
        if not self.bFreeze:  
            for d in self.dragons:
                d.update()
                d.hone_in(self.ship.x, self.ship.y)
                d.animate()
        for s in sparks:
            s.update()

	    #render objects	  
        self.ship.render()
        rabbyt.render_unsorted(self.dragons)
        rabbyt.render_unsorted(self.bullets)
        rabbyt.render_unsorted(sparks)
	    #render font
        text_score.render()
        text_boost.render()
        text_health.render()
        text_chronos.render()

        text_health.text = "Health: " + str(self.health)
	if self.fuel < MAX_FUEL:
	    self.fuel += FUEL_REGAIN
            text_boost.text = "Boost Fuel: " + str(self.fuel)
	else:
            self.fuel = 100.0
            text_boost.text = "Boost Fuel: " + str(self.fuel)

        self.clock.tick(40)
        pygame.display.flip()
