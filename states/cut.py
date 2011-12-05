"""
The First Cutscene
"""
from __future__ import division
import pygame
import rabbyt
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_ESCAPE

from settings import FontSprite
import state
import states.name

if not pygame.mixer: 
    print 'Warning, sound disabled'

#def CutScreen(game, state_stack):
class Cut(state.State):
    """The Cutscene Class"""
    def run(self, game, state_stack):
        """Makes the Cutscene run"""

        game.set_state_time()
        scene = rabbyt.Sprite("1cutscene.png")
        scene.scale = 0.95
        scene.y = -60
        scene.alpha = rabbyt.lerp(0.0, 0.8, startt=1, endt=8)
        scene.x = rabbyt.lerp(-20, 60, startt=1, endt=6)

        scene2 = rabbyt.Sprite("1cutscene2.png")
        scene2.alpha = rabbyt.lerp(0.8, 0.0, startt=6, endt=13)
        scene2.scale = 0.95
        scene2.xy = (60, -60)

        words = FontSprite(game.font, "Scientist: I'll be back soon.")
        words.xy = (-195, -250)

        #set music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('scene1.mp3')
        pygame.mixer.music.play()

        game.done = False
        while not game.done:
            rabbyt.clear()
            rabbyt.set_time(game.get_ticks()/1000.0)
            ticks = game.get_ticks()/1000.0
            if ticks < 6:
                scene.render()
            if ticks >= 6:
                scene2.render()
            if ticks >= 14:
                game.done = True
                state_stack.append(states.name.Name())
            words.render()

            for event in pygame.event.get():
                if event.type ==  QUIT:
                    game.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(game.high_score_names[i] + " " \
                                    + str(game.high_scores[i]) + "\n")
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_RETURN:
                        game.done = True
                        state_stack.append(states.name.Name())
            pygame.display.flip()
