"""
Game State for Rabbit Hole
"""
from __future__ import division
import pygame, rabbyt
import states.menu, states.cut, states.name, states.highscore
import user_data
import os
from settings import Font
import states.cuttwo
if not pygame.mixer: 
    print 'Warning, sound disabled'

SCREEN_SIZE = (800, 600)
STARTING_SCREEN = "Menu Screen"

class Game:
    """ Game class acts as motherboard for game """
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, \
		              pygame.OPENGLBLIT | pygame.DOUBLEBUF)
        rabbyt.set_viewport(SCREEN_SIZE)
        rabbyt.set_default_attribs()

        #self.game_state = [STARTING_SCREEN] ## A stack of game screens.

        self.temp_score = 0
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.previous_tick_count = pygame.time.get_ticks()

        self.font = Font(pygame.font.Font(None, 36))

        #title state
        self.backg = pygame.Surface(self.screen.get_size()).convert()
        #self.numCalled = 0

        #high scores
        self.winner_name = ""
        self.high_scores = []
        self.high_score_names = []

        self.user = user_data.User()

        if not os.path.isfile("RabbitHighScores"):
            self.high_scores = ['0', '0', '0', '0', '0']
            self.high_score_names = ["OKW", "KRW", "ON", "DL", "AAA"] 
            fdata = open("RabbitHighScores", 'w')
            fdata.write("OKW 0\nKRW 0\nON 0\nDL 0\nAAA 0")
        else:
            fdata = open("RabbitHighScores")
            for line in fdata.readlines():
                temp = line.split()
                self.high_scores.append(int(temp[1]))
                self.high_score_names.append(temp[0])

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

        #time
        self.time_offset = 0.0


    def start(self):
        """ Starts the game """
        keep_going = True
        while keep_going:
            if not self.game_states:
                break
            
            #temporary loop to determine next state to call.
            next_state = self.game_states.pop()
            next_state.run(self, self.game_states)

    def update_scores(self):
        """Updates the high scores"""
        def calculate_high_score():
            """Calculates the high scores"""
            for i in range(len(self.high_scores)-1):
                if self.high_scores[i] >= self.user.score and \
		    self.user.score >= self.high_scores[i+1]:
                    return i

        index = calculate_high_score()

        if index == None:
            if self.high_scores[0] <= self.user.score:
                self.high_scores.insert(0, self.user.score)
                self.high_score_names.insert(0, self.winner_name)
            del self.high_scores[5]
            del self.high_score_names[5]
        else:
            self.high_scores.insert(index+1, self.user.score)
            self.high_score_names.insert(index+1, self.winner_name)
            del self.high_scores[5]
            del self.high_score_names[5]


    def set_state_time(self):
        """Resets the time"""
        self.time_offset = pygame.time.get_ticks()
        print "new time_offset: ", self.time_offset

    def get_ticks(self):
        """Reimplementation of pygame.time.get_ticks()"""
        return pygame.time.get_ticks() - self.time_offset

## Run the demo.
pygame.init()
GAME = Game()
GAME.start()
