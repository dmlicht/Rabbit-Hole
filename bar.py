from __future__ import division
import pygame, rabbyt

class Bar():
    def __init__(self):
	#health bar
	self.bar                     = rabbyt.Sprite(0, (0,20,200,0))
	self.bar.rgb                 = (34,139,34)
	self.bar.xy                  = (200, -240)

    def hit(self):
	if self.bar.shape[2][0] > 0:
            temp = self.bar.shape
            self.bar.shape = (0,temp[1][1],temp[2][0]-20,0)

    def render(self):
	self.bar.render()