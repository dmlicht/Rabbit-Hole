from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *

import os, random
import settings
import player, enemy, bullet, chronos, Boss1
from settings import Font, FontSprite


def CutTwo(game, state_stack):
    clock = pygame.time.Clock()
    scene = rabbyt.Sprite("1space.png")
    scene.scale = 2.0
    scene.x = 400
    rabbit = rabbyt.Sprite("1rabbit.png")
    #scene.alpha = rabbyt.lerp(0.0, 0.8, startt=1, endt=30)
    #scene.x = rabbyt.lerp(-20, 60, startt=1, endt=6)

    rabbit.alpha = rabbyt.lerp(0.0, 1.0, startt=3, endt=5)
    rabbit.scale = 0.5
    #rabbit.xy = (60,-60)

    words = FontSprite(game.font, "Dimensional Rabbit: ZzZzz ...")
    words.alpha = rabbyt.lerp(0.0, 1.0, startt=3, endt=5)
    words.y = -250
    words.x = -180;

    game.done = False
    while not game.done:
        clock.tick(40)
        rabbyt.clear()
	scene.render()
        rabbyt.set_time(pygame.time.get_ticks()/1000.0)
        ticks = pygame.time.get_ticks()/1000.0
        if ticks >= 3:
           words.render()
           rabbit.render()
        if ticks >= 5 and ticks < 7:
           words.x = -200;
           words.text = "Dimensional Rabbit: ZZzzZ ZZzz ..."
        elif ticks >= 7 and ticks < 9:
           words.text = "Dimensional Rabbit: Oh!"
           words.x = -160;
        elif ticks >= 9 and ticks < 11:
           words.text = "Dimensional Rabbit: I didn't think ..."
           words.x = -260;
        elif ticks >= 11 and ticks < 13:
           words.text = "Dimensional Rabbit: ... anybody would make it this far"
           words.x = -330;
        elif ticks >= 13 and ticks < 17:
           words.text = "Dimensional Rabbit: Pardon me, you look lost."
           words.x = -270;
        elif ticks >= 17 and ticks < 21:
           words.text = "Scientist: I know exactly where I'm going."
           words.x = -250;
        elif ticks >= 21 and ticks < 25:
           words.text = "Dimensional Rabbit: Then you won't be needing help from me."
           words.x = -385;
        elif ticks >= 25 and ticks < 29:
           words.text = "Dimensional Rabbit: Tata!"
           words.x = -160;
           rabbit.alpha = rabbyt.lerp(1.0, 0.0, startt=25, endt=29)
        elif ticks >= 29:
           words.text = "Scientist: ..."
           words.x = -100;
           scene.alpha = rabbyt.lerp(1.0, 0.0, startt=29, endt=33)
        if ticks >= 33:
            game.done = True
            state_stack.append("Level Two")

        for event in pygame.event.get():
            if event.type ==  QUIT:
                game.done = True
                fdata = open("RabbitHighScores", 'w')
                for i in range(5):
                    fdata.write(game.highScoreNames[i] + " " + str(game.highScores[i]) + "\n")
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_SPACE:
                    game.done = True
                    state_stack.append("Name Screen")
        pygame.display.flip()
