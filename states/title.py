"""
The Title Screen
"""
from __future__ import division
import pygame, rabbyt
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_ESCAPE

def TitleScreen(self, state_stack):
    """ Title Screen"""
    self.frame = 0 
    self.done = False

    """rabbit_screen = rabbyt.Sprite
    ('8jumping_rabbit.png', (-321,184.5,321,-184.5))
    rabbit_tex_shapes = settings.get_tex_shapes(rabbit_screen.tex_shape, 8)"""

    while not self.done:
        self.clock.tick(40)

        if pygame.time.get_ticks() - self.fps > 1000:
            print "FPS: ", self.clock.get_fps()
            self.fps = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                    fdata = open("RabbitHighScores", 'w')
                    for i in range(5):
                        fdata.write(self.highScoreNames[i] + \
                                    " " + str(self.highScores[i]) + "\n")
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                        fdata = open("RabbitHighScores", 'w')
                        for i in range(5):
                            fdata.write(self.highScoreNames[i] + \
                                        " " + str(self.highScores[i]) + "\n")

                    ## Some sample reaction to events.
                    elif event.key == K_SPACE:
                        ## This screen will end and go to another screen.
                        self.done = True
                        state_stack.append("Menu Screen")

        rabbyt.set_time(pygame.time.get_ticks()/1000.0)
        rabbyt.scheduler.pump()
        rabbyt.clear()

        #self.animate(rabbit_screen, rabbit_tex_shapes)
        #rabbit_screen.render()

        pygame.display.flip()
 
