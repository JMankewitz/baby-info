# from https://github.com/esdalmaijer/PyGaze/blob/master/examples/pygaze_trackertest/PyGaze_trackertest.py

# This script tests all eyetracker functions of PyGaze; run it to see if
# your installation is working as it is supposed to. Remember to adjust the
# constants in the attached constants.py script to the relevant values for
# your system and preference!
#
# contents of the directory in which this script should come:
# PyGaze_supertest.py (this script)
# constants.py (script containing constants)
# bark.ogg (soundfile)
# kitten.png (image file)
#
# version: 22 Dec 2013


import os
import random

from pygaze.defaults import *
from constants import *

from pygaze.display import Display
from pygaze.screen import Screen
from pygaze.eyetracker import EyeTracker
from pygaze.keyboard import Keyboard

from pygaze.time import Time
from pygaze.logfile import Logfile

from pygaze.plugins.aoi import AOI



# # # # #
# create instances

# initialize the display
disp = Display()

# initialize a screen
scr = Screen()

# initialize an EyeTracker
tracker = EyeTracker(disp)

# initialize a keyboard
kb = Keyboard(keylist=['space'],timeout=None)


# initialize a Timer
timer = Time()

# create a new logfile
log = Logfile(filename="test")
log.write(["test", "time"])


# # # # #
# welcome
print(tracker.connected())
scr.draw_text("Welcome to the PyGaze Supertest!\n\nYou're going to be testing \
your PyGaze installation today, using this interactive tool. Press Space \
to start!\n\n\nP.S. If you see this, the following functions work: \
\n- Screen.draw_text \
\n- Disp.fill \
\n- Disp.show \
\nAwesome!", color = "white", fontsize = 12)
#scr.draw_text(text = "Loading Files...", color = "white", fontsize = 48)
disp.fill(scr)
t1 = disp.show()
log.write(["welcome", t1])
kb.get_key()


# # # # #
# test EyeTracker

print(tracker.connected())
#EyeTracker.log_var
#EyeTracker.pupil_size
#EyeTracker.send_command
#EyeTracker.wait_for_event

scr.clear()
scr.draw_text("We're now going to test the eyetracker module. Press Space to start!", color = "white", fontsize = 12)
disp.fill(scr)
t1 = disp.show()
log.write(["EyeTracker", t1])
kb.get_key()

# tracker.calibrate
tracker.calibrate()

# tracker.sample()
scr.clear()
scr.draw_text("The dot should follow your eye movements",color = "white", fontsize = 12)
disp.fill(scr)
disp.show()
tracker.log("now testing sample function")
tracker.status_msg("now testing sample function")
tracker.start_recording()
key = None
while not key == 'space':
    # get new key
    key, presstime = kb.get_key(timeout=1)
    # new states
    gazepos = tracker.sample()
    print(gazepos)
    # draw to screen
    scr.clear()
    scr.draw_text("The dot should follow your eye movements",color = "white",fontsize = 21)
    scr.draw_fixation(fixtype='dot', colour = "red", pos=gazepos, pw=3, diameter=15)
    disp.fill(scr)
    disp.show()
tracker.stop_recording()
scr.clear()