from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *
import os, random
import settings
from settings import Font, FontSprite
import player, enemy, bullet, chronos, Boss1

def MenuScreen(game, state_stack):
  if True:
    backg = rabbyt.Sprite('1Menu_Screen1.png') 
    menu_option = 0
    text1 = FontSprite(game.font, "Start Game")
    text2 = FontSprite(game.font, "Adjust Sound")
    text3 = FontSprite(game.font, "Adjust Brightness")
    text4 = FontSprite(game.font, "High Scores")
    text5 = FontSprite(game.font, "Quit")
    text1.xy = (-65, 100)
    text2.xy = (-80,50)
    text3.xy = (-110,0)
    text4.xy = (-77,-50)
    text5.xy = (-22,-100)

    game.done = False
    while not game.done:
      rabbyt.clear()
      backg.render()
      text1.render()
      text2.render()
      text3.render()
      text4.render()
      text5.render()

      for event in pygame.event.get():
        if event.type == QUIT:
          game.done = True
          fdata = open("RabbitHighScores", 'w')
          for i in range(5):
            fdata.write(game.highScoreNames[i] + " " + str(game.highScores[i]) + "\n")
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            game.done = True
            fdata = open("RabbitHighScores", 'w')
            for i in range(5):
              fdata.write(game.highScoreNames[i] + " " + str(game.highScores[i]) + "\n")

        ## Some sample reaction to events.
          elif event.key == K_SPACE:
            if menu_option == 0:
              game.done = True
              state_stack.append("Cut Screen")
            elif menu_option == 1:
              game.done = False
            elif menu_option == 2:
              game.done = False
            elif menu_option == 3:
              game.done = True
              state_stack.append("High Screen")
            elif menu_option == 4:
              game.done = True
          elif event.key == K_DOWN:
            if menu_option < 4:
              menu_option += 1
            else:
              menu_option = 0
          elif event.key == K_UP:
            if menu_option > 0:
              menu_option -= 1
            else:
              menu_option = 4        

      if menu_option == 0:
        text5.rgb = (255,255,255)
        text1.rgb = (0,0,0)
        text2.rgb = (255,255,255)
      elif menu_option == 1:
        text1.rgb = (255,255,255)
        text2.rgb = (0,0,0)
        text3.rgb = (255,255,255)
      elif menu_option == 2:
        text2.rgb = (255,255,255)
        text3.rgb = (0,0,0)
        text4.rgb = (255,255,255)
      elif menu_option == 3:
        text3.rgb = (255,255,255)
        text4.rgb = (0,0,0)
        text5.rgb = (255,255,255)
      elif menu_option == 4:
        text4.rgb = (255,255,255)
        text5.rgb = (0,0,0)
        text1.rgb = (255,255,255)

      pygame.display.flip()
      game.clock.tick(40)
      #game.done = False
