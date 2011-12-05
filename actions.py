import pygame

class Actions():
    def __init__(self):
        self.up                 = False
        self.down               = False
        self.left               = False
        self.right              = False
        self.fire               = False
        self.tilt_left          = False
        self.tilt_right         = False
       	self.boost              = False
        self.toggle_time_travel = False
       	self.ticks              = -1