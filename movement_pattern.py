## beginning of import
from __future__ import division
import rabbyt

def straight_down(start, time=4):
    return rabbyt.ease(start, start-800, dt=time)

def straight_down1(start):
    return straight_down(start, 3.5)

def straight_down2(start):
    return straight_down(start, 3.0)

def straight_down3(start):
    return straight_down(start, 2.75)

def straight_down4(start):
    return straight_down(start, 2.5)

def straight_down5(start):
    return straight_down(start, 2.25)

def straight_down6(start):
    return straight_down(start, 2.0)

def straight_down7(start):
    return straight_down(start, 1.75)

def straight_down8(start):
    return straight_down(start, 1.5)

def straight_down9(start):
    return straight_down(start, 1.25)

def straight_across(start, time=4):
    return rabbyt.ease(start, start+800, dt=time)

def straight_across1(start):
    return straight_across(start, 3.5)

def straight_across2(start):
    return straight_across(start, 3.0)

def straight_across3(start):
    return straight_across(start, 2.75)

def straight_across4(start):
    return straight_across(start, 2.5)

def straight_across5(start):
    return straight_across(start, 2.25)

def straight_across6(start):
    return straight_across(start, 2.0)

def straight_across7(start):
    return straight_across(start, 1.75)

def straight_across8(start):
    return straight_across(start, 1.5)

def straight_across9(start):
    return straight_across(start, 1.25)

def back_and_forth(start, time=4):
    return rabbyt.lerp(start, start+600, dt=time, extend="reverse")

def back_and_forth1(start):
    return back_and_forth(start, 8)

def do_nothing(start):
    return rabbyt.lerp(start, start, dt=1)

def movpatternx(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=1),
                         rabbyt.lerp(startx+50, startx, dt=1),
                         rabbyt.lerp(startx, startx-200, dt=1, 
                         extend="reverse"),)

def movpatterny(start):
    return rabbyt.chain( rabbyt.ease(start, start-400, dt=1),
                         rabbyt.ease(start-400, start-200, dt=2),
                         rabbyt.ease(start-200, start-400, dt=1, 
                         extend="reverse"),)
def movpatternx1(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=1),
                         rabbyt.lerp(startx+50, startx-50, dt=1),
                         rabbyt.lerp(startx-50, startx, dt=1, 
                         extend="reverse"),)

def movpatterny1(start):
    return rabbyt.chain( rabbyt.lerp(start, start-600, dt=2),
                         rabbyt.lerp(start-600, start-500, dt=1),
                         rabbyt.lerp(start-500, start-800, dt=2, 
                         extend="reverse"),)

def movpatternx2(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+100, dt=1.5),
                         rabbyt.lerp(startx+100, startx-100, dt=3),
                         rabbyt.lerp(startx-100, startx, dt=1.5, 
                         extend="reverse"),)

def movpatterny2(start):
    return rabbyt.chain( rabbyt.lerp(start, start-400, dt=4),
                         rabbyt.lerp(start-400, start, dt=4, 
                         extend="reverse"),)

def movpattern_circx(startx):
    return startx+rabbyt.chain( rabbyt.lerp(0, 100, dt=1),
                         rabbyt.lerp(100, -100, dt=2),
                         rabbyt.lerp(-100, 0, dt=1, extend="reverse"),)

def movpattern_circy(start):
    return start+rabbyt.chain( rabbyt.lerp(-100, 0, dt=1),
                         rabbyt.lerp(0, 100, dt=1),
                         rabbyt.lerp(100, -100, dt=2, extend="reverse"),)

def boss1_pat(start):
    return rabbyt.chain( rabbyt.lerp(start, start-600, dt=3),
                         rabbyt.lerp(start-600, start, dt=3,
                         extend="reverse"),)

def boss_hand1_patx(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx-200, dt=0.5),
                         rabbyt.lerp(startx-200, startx, dt=0.5, 
                         extend="reverse"),)

def boss_hand2_patx(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+200, dt=0.5),
                         rabbyt.lerp(startx+200, startx, dt=0.5, 
                         extend="reverse"),)

def boss2_patx(startx):
    return rabbyt.chain( rabbyt.lerp(startx, startx+250, dt = 1),
                         rabbyt.lerp(startx+250, startx-250, dt = 2),
                         rabbyt.lerp(startx+250, startx, dt = 1),
                         rabbyt.lerp(startx+250, startx, dt = 1),
                         rabbyt.lerp(startx+250, startx-250, dt = 2),
                         rabbyt.lerp(startx, startx+250, dt = 1,
                         extend="reverse"),)

def boss2_paty(starty):
    return rabbyt.chain( rabbyt.lerp(starty, starty-600, dt=1),
                         rabbyt.lerp(starty-600, starty-300, dt=0.5),
                         rabbyt.lerp(starty-300, starty-600, dt = 0.5),
                         rabbyt.lerp(starty-600, starty, dt = 1),
                         rabbyt.lerp(starty, starty-600, dt = 1),
                         rabbyt.lerp(starty-600, starty-300, dt = 0.5),
                         rabbyt.lerp(starty-300, starty-600, dt=0.5),
                         rabbyt.lerp(starty-600, starty, dt=1),
                         rabbyt.lerp(starty, starty-600, dt=1),
                         rabbyt.lerp(starty-600, starty-600, dt = 3.5),
                         rabbyt.lerp(starty-600, starty-350, dt = 0.5),
                         rabbyt.lerp(starty-350, starty-350, dt = 3.5),
                         rabbyt.lerp(starty-350, starty, dt = 0.5,
                         extend="reverse"),)

"""def pattern3(startx, starty):
    return (rabbyt.chain( rabbyt.lerp(startx, startx+50, dt=3/2),
                           rabbyt.lerp(startx+50, startx, dt=3/2),
                           rabbyt.lerp(startx, startx-50, dt=3/2, 
                           extend="reverse"),)), \
                           (rabbyt.chain( rabbyt.lerp(self.y, self.y-300, dt=2),
                           rabbyt.lerp(self.y-300, self.y-150, dt=2),
                           rabbyt.lerp(self.y-150, self.y-450, dt=2),
                           rabbyt.lerp(self.y-450, self.y-400, dt=2),
                           rabbyt.lerp(self.y-400, self.y-1000, dt=2, 
                           extend="reverse"),))
"""
