import pygaze
import psychopy
from psychopy import visual
from pygaze import libscreen, libinput, eyetracker, libtime

import constants
import tobii_research as tr

exp_length = 10000

t0 = libtime.get_time()

disp = libscreen.Display(disptype='psychopy', fgc="black", bgc="black")
win = pygaze.expdisplay

eyetrackers = tr.find_all_eyetrackers()
print(eyetrackers)
tracker = pygaze.eyetracker.EyeTracker(disp)
#

eyetrackers[0]
# tracker.connected()
#
connected_bool = tracker.connected()
print(connected_bool)
#
# x_length = constants.DISPSIZE[0]
# y_length = constants.DISPSIZE[1]
# print(x_length, y_length)
#
# while libtime.get_time() - t0 < exp_length:
#
#     curGazePos = tracker.sample()
#     psychopy_pos_x = curGazePos[0] - (x_length/2)
#     psychopy_pos_y = (curGazePos[1] - (y_length/2)) *-1
#     gazedot = visual.GratingStim(win,tex=None, mask="gauss",
#                                      pos=(psychopy_pos_x, psychopy_pos_y),size=(66,66),color='green')
#     gazedot.draw()
#     win.flip()
#     print(curGazePos)


