"""
The Fifth Cutscene
"""
from __future__ import division
import pygame
import rabbyt
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_ESCAPE

from settings import FontSprite
import state
import states.highscore

if not pygame.mixer: 
    print 'Warning, sound disabled'

#def CutScreen(game, state_stack):
class CutFive(state.State):
    """The Cutscene Class"""
    def run(self, game, state_stack):
        """Makes the Cutscene run"""

        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('scene5.wav')
        pygame.mixer.music.play(-1, 0.0)

        game.set_state_time()
        scene = rabbyt.Sprite("1cutscene.png")
        scene.scale = 0.95
        scene.y = -60
        scene.alpha = rabbyt.lerp(0.0, 0.8, startt=1, endt=10)
        scene.x = rabbyt.lerp(-20, 60, startt=1, endt=10)

        scene2 = rabbyt.Sprite("1cutscene2.png")
        scene2.alpha = rabbyt.lerp(0.8, 0.0, startt=10, endt=22)
        scene2.scale = 0.95
        scene2.xy = (60, -60)

        words = FontSprite(game.font, "Girlfriend: You're Back!")
        words.xy = (-150, -250)

        game.done = False
        while not game.done:
            rabbyt.clear()
            rabbyt.set_time(game.get_ticks()/1000.0)
            ticks = game.get_ticks()/1000.0
            if ticks < 10:
                scene.render()
            else:
                scene2.render()    
            
            if ticks >= 6 and ticks < 10:
                words = FontSprite(game.font, "Scientist: I'm back!")
                words.xy = (-150, -250)
            elif ticks >= 10 and ticks < 14:
                words = FontSprite(game.font, "Scientist: And I brought flowers!")
                words.xy = (-200, -250)
            elif ticks >= 14 and ticks <18:
                words = FontSprite(game.font, "Girlfriend: And you brought flowers!")
                words.xy = (-220, -250)
            elif ticks >= 18 and ticks <22:
                words = FontSprite(game.font, "Scientist: Do you want to go back for more?")
                words.xy = (-270, -250)
            if ticks >= 22:
                game.done = True
                state_stack.append(states.highscore.High())
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
                        state_stack.append(states.highscore.High())
                elif event.type == pygame.JOYBUTTONDOWN and game.joystick.get_button(game.controls.settings["Escape"]):
                    game.done = True
                    state_stack.append(states.highscore.High())
            pygame.display.flip()

