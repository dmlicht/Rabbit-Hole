from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random, copy
import tiles, layout
import settings
import player, enemy, bullet, chronos, Boss1, Boss0, BossHands
from settings import Font, FontSprite

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

def PlayScreen(self, state_stack):

    self.score = 0

    background = tiles.Background(SCREEN_WIDTH, SCREEN_HEIGHT, "sample_tile_layout.txt")
    background.initialize()

    self.ret_count = 0
    self.boss_count = 0
    self.energy = 100
    self.health = 3

    clock = pygame.time.Clock() 

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
    
    #players
    self.ship = player.Ship("3ship1", self.screen)

    self.f_xy = []

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
        pressed = pygame.key.get_pressed()

        #ship boost
        if pressed[K_d]:
            self.ship.boosting = True
        else: self.ship.boosting = False
        text_boost.text = "Boost Fuel: " + str(self.ship.boost_fuel)

	    #ship animation
        if pressed[K_UP] != 0 or pressed[K_DOWN] != 0 or pressed[K_LEFT] != 0 or pressed[K_RIGHT] != 0:
            self.ship.animate()

	    #Vertical Movement
        self.ship.acceleration_y = pressed[K_UP] - pressed[K_DOWN]
        self.ship.check_vertical_bounds()

	    #Horizontal Movement
        self.ship.acceleration_x = pressed[K_RIGHT] - pressed[K_LEFT]
        self.ship.check_horizontal_bounds()

        #tilt
        self.ship.tilt = pressed[K_z] - pressed[K_x]
        if pressed[K_SPACE] and not self.bHaveFired:
            fired_bullet = bullet.Bullet(self.screen, self.ship.xy, self.ship.rot, 10)
            self.bullets.append(fired_bullet)
            self.bHaveFired = True

        rabbyt.set_time(pygame.time.get_ticks()/1000.0)
        rabbyt.scheduler.pump()
        rabbyt.clear()

        #background handling
        background.maintain_tile_rows()
        
        self.ship.update()

        background.render()
        self.ship.render()
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
