import pygame as PG
import pygame.joystick as PJ
import pygame.event as PE
import sys

PG.init()

print PJ.get_count()

joy = PJ.Joystick(0)
joy.init()

print "Name", joy.get_name()
print "Hats", joy.get_numhats()
print "Buttons", joy.get_numbuttons()
print "Axes", joy.get_numaxes()
print "Balls", joy.get_numballs()

while True:
   events = PE.get()
   for event in events:
      if event.type == QUIT:
         sys.quit()

   print pygame.JOYBUTTONUP