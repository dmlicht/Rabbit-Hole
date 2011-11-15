from __future__ import division
import pygame, rabbyt, sys
from pygame.locals import *
import states.menu, states.cut, states.name, states.highscore, states.title
import user_data
import os, random
#rabbyt.data_directory = os.path.dirname(__file__)
#os.environ["SDL_VIDEO_CENTERED"] = "1"
import settings
import player, enemy, bullet, chronos
from settings import Font, FontSprite
import states.cuttwo

if not pygame.mixer: print 'Warning, sound disabled'

SCREEN_SIZE = (800,600)
STARTING_SCREEN = "Menu Screen"

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.OPENGLBLIT | pygame.DOUBLEBUF)
        rabbyt.set_viewport(SCREEN_SIZE)
        rabbyt.set_default_attribs()

        #self.game_state = [STARTING_SCREEN] ## A stack of game screens.

        self.temp_score = 0
        self.font = pygame.font.Font(None,24)
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.previous_tick_count = pygame.time.get_ticks()

        self.font = Font(pygame.font.Font(None, 36))

        #title state
        self.backg = pygame.Surface(self.screen.get_size()).convert()
        self.numCalled = 0

        #high scores
        self.winner_name = ""
        self.highScores = []
        self.highScoreNames = []

        self.user = user_data.User()

	if not os.path.isfile("RabbitHighScores"):
            self.highScores = ['0','0','0','0','0']
            self.highScoreNames = ["OKW","KRW", "ON", "DL", "AAA"] 
            fdata = open("RabbitHighScores", 'w')
            fdata.write("OKW 0\nKRW 0\nON 0\nDL 0\nAAA 0")
        else:
            fdata = open("RabbitHighScores")
            for line in fdata.readlines():
                temp = line.split()
                self.highScores.append(int(temp[1]))
                self.highScoreNames.append(temp[0])

        #music
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        #self.crash = pygame.mixer.Sound('Crash1.wav')
        self.win_sound = pygame.mixer.Sound('winning16bit.wav')
        self.lose_sound = pygame.mixer.Sound('losing16bit.wav')
        self.gem_pickup_sound = pygame.mixer.Sound('gem.wav')

        #pygame.mixer.music.load('game-motif-sad.mp3')
        #pygame.mixer.music.play(-1, 0.0)

        self.game_states = []
        self.done = False
        self.game_states.append(states.menu.Menu())

    def Go(self):
        keep_going = True
        while keep_going:
            if not self.game_states:
                break
            
            #temporary loop to determine next state to call.
            next_state = self.game_states.pop()
            next_state.run(self, self.game_states)

    def animate(self, sprite, frames):
        #animation
        current_tick_count = pygame.time.get_ticks() 
        clock_ticks_since_check = current_tick_count - self.previous_tick_count
        constant = 150

        if clock_ticks_since_last_check > constant: 
            if self.frame < len(frames) - 1: 
                self.frame += 1 
                sprite.tex_shape = frames[self.frame]
            else:
                self.frame = 0 
            self.previous_tick_count = now 

    def update_scores(self):
        def calculate_high_score():
            for i in range(len(self.highScores)-1):
                if self.highScores[i] >= self.score and self.score >= self.highScores[i+1]:
                    return i

        index = calculate_high_score()

        if index == None:
            if self.highScores[0] <= self.score:
                self.highScores.insert(0, self.score)
                self.highScoreNames.insert(0, self.winner_name)
	        del self.highScores[5]
	        del self.highScoreNames[5]
        else:
            self.highScores.insert(index+1, self.score)
            self.highScoreNames.insert(index+1, self.winner_name)
            del self.highScores[5]
            del self.highScoreNames[5]

    def set_state_time(self):
        self.time_offset = pygame.time.get_ticks()
        print "new time_offset: ", self.time_offset

    def get_ticks(self):
        return pygame.time.get_ticks() - self.time_offset

## Run the demo.
pygame.init()
g = Game()
g.Go()
