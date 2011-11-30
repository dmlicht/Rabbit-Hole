"""
The Second Cutscene
"""
from __future__ import division
import pygame
import rabbyt
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_ESCAPE

import state, states.level
import states.cutfive
from settings import FontSprite

#def CutTwo(game, state_stack):
class CutFour(state.State):
    """The Second Cutscene"""
    def run(self, game, state_stack):
        """Starts the cutscene"""
        clock = pygame.time.Clock()
        self.game = game
        game.set_state_time()
        scene = rabbyt.Sprite("1space.png")
        scene.scale = 2.0
        scene.x = 400
        rabbit = rabbyt.Sprite("1rabbit.png")
        self.state_stack = state_stack
        #scene.alpha = rabbyt.lerp(0.0, 0.8, startt=1, endt=30)
        #scene.x = rabbyt.lerp(-20, 60, startt=1, endt=6)

        rabbit.alpha = rabbyt.lerp(0.0, 1.0, startt=3, endt=5)
        rabbit.scale = 0.5
        #rabbit.xy = (60,-60)

        words = FontSprite(game.font, "Dimensional Rabbit: Oh ...")
        words.alpha = rabbyt.lerp(0.0, 1.0, startt=3, endt=5)
        words.y = -250
        words.x = -180

        game.done = False
        while not game.done:
            clock.tick(40)
            rabbyt.clear()
            scene.render()
            rabbyt.set_time(game.get_ticks()/1000.0)
            ticks = game.get_ticks()/1000.0
            if ticks >= 3:
                words.render()
                rabbit.render()
            if ticks >= 5 and ticks < 7:
                words.x = -200
                words.text = "Dimensional Rabbit: It's you again ..."
            elif ticks >= 7 and ticks < 9:
                words.text = "Scientist: THAT WAS THE WRONG TIME"
                words.x = -160
            elif ticks >= 9 and ticks < 11:
                words.text = "Scientist: WHY'D you lead me to WW2?!"
                words.x = -260
            elif ticks >= 11 and ticks < 13:
                words.text = "Dimensional Rabbit: So I was off" + \
                             " by like 500 years."
                words.x = -330
            elif ticks >= 13 and ticks < 17:
                words.text = "Dimensional Rabbit: Do you know how many " + \
                             "portals there are"
                words.x = -380
            elif ticks>=17 and ticks < 21:
                words.text = "Dimensional Rabbit: in this place?"
                words.x = -100
            elif ticks >= 21 and ticks < 25:
                words.text = "Scientist: Well can you tell me where now?"
                words.x = -250
            elif ticks >= 25 and ticks < 29:
                words.text = "Dimensional Rabbit: Yeah it's this one " + \
                             "for sure."
                words.x = -315
            elif ticks >= 29 and ticks < 33:
                words.text = "Dimensional Rabbit: Sorry about the mix up. Good luck!"
                words.x = -300
                rabbit.alpha = rabbyt.lerp(1.0, 0.0, startt=25, endt=29)
            elif ticks >= 33:
                words.text = "Scientist: I hope you're right this time!"
                words.x = -200
                scene.alpha = rabbyt.lerp(1.0, 0.0, startt=29, endt=33)
            if ticks >= 37:
                game.done = True
                self.set_next_state()

            for event in pygame.event.get():
                if event.type ==  QUIT:
                    game.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(game.high_score_names[i] +  \
                                    " " + str(game.high_scores[i]) + "\n")
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_RETURN:
                        game.done = True
                        self.set_next_state()
            pygame.display.flip()

    def set_next_state(self):
        """Makes Next State"""
        self.state_stack.append(states.level.Level( \
          self.game, "level4.txt", states.cutfive.CutFive()))
